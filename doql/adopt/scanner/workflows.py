"""Workflow scanning — Makefile, Taskfile.yml, and Python CLI commands."""
from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from ...parsers.models import DoqlSpec, Workflow, WorkflowStep
from .utils import load_yaml, walk_files

# Targets that are *meta* scaffolding, not user-facing workflows. Excluding
# them keeps the generated ``workflow[...]`` section focused on meaningful
# automation (build/test/deploy/lint/...).
_MAKEFILE_SKIP_TARGETS = {
    "all", "default", ".phony", ".default", "help",
}

# CLI commands that should become workflows automatically
_CLI_WORKFLOW_COMMANDS = {
    "analyze": {"tools": "code2llm,redup,vallm", "desc": "Run project analysis tools"},
    "test": {"desc": "Run test suite"},
    "lint": {"desc": "Run linting"},
    "format": {"desc": "Format code"},
    "build": {"desc": "Build project"},
    "deploy": {"desc": "Deploy application"},
}


def scan_workflows(root: Path, spec: DoqlSpec) -> None:
    """Promote Makefile / Taskfile.yml targets and Python CLI commands to ``WORKFLOW`` blocks.

    Workflows detected here are *non-authoritative* — they mirror the shell
    automation the project already has so that a downstream ``doql build``
    can regenerate equivalent scripts. Each target becomes a ``Workflow``
    with the command lines captured as ``run cmd=...`` steps.
    """
    makefile = root / "Makefile"
    if makefile.exists():
        _extract_makefile_workflows(makefile, spec)

    for taskfile_name in ("Taskfile.yml", "Taskfile.yaml"):
        tf_path = root / taskfile_name
        if tf_path.exists():
            _extract_taskfile_workflows(tf_path, spec)
            break

    # Scan Python CLI commands for workflow candidates
    _extract_python_cli_workflows(root, spec)


# Makefile target regex - see _extract_makefile_workflows for details
_TARGET_RE = re.compile(
    r"^([a-zA-Z_][a-zA-Z0-9_-]*)[ \t]*:(?!=)[ \t]*([^\n]*)\n((?:\t[^\n]+\n?)*)",
    re.MULTILINE,
)


def _is_valid_target(name: str, deps_raw: str, seen: set[str]) -> bool:
    """Validate that a target name is acceptable (not skip target, not seen, not var)."""
    if name.startswith(".") or name.lower() in _MAKEFILE_SKIP_TARGETS:
        return False
    if name in seen:
        return False
    if deps_raw.lstrip().startswith("="):
        return False
    return True


_HEREDOC_START_RE = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?")


def _build_steps_from_body(body: str, deps_raw: str) -> list[WorkflowStep]:
    """Build workflow steps from Makefile command body and dependencies."""
    steps: list[WorkflowStep] = []
    in_heredoc = False
    heredoc_marker: str | None = None
    for line in body.splitlines():
        cmd = line.strip()
        if cmd.startswith("@"):
            cmd = cmd[1:]
        if not cmd:
            continue
        if not in_heredoc and "<<" in cmd:
            match = _HEREDOC_START_RE.search(cmd)
            heredoc_marker = match.group(1) if match else "EOF"
            in_heredoc = True
            steps.append(WorkflowStep(action="run", params={"cmd": cmd}))
            continue
        if in_heredoc:
            if cmd.rstrip(";") == heredoc_marker or cmd == heredoc_marker:
                in_heredoc = False
                heredoc_marker = None
            continue
        steps.append(WorkflowStep(action="run", params={"cmd": cmd}))
    # Promote prerequisites to explicit depend steps
    deps = _parse_makefile_deps(deps_raw)
    if deps and not steps:
        for dep in deps:
            steps.append(WorkflowStep(action="depend", params={"target": dep}))
    return steps


def _create_workflow(name: str, steps: list[WorkflowStep]) -> Workflow | None:
    """Create a Workflow if steps exist, otherwise return None."""
    if not steps:
        return None
    return Workflow(name=name, trigger="manual", steps=steps)


def _extract_makefile_workflows(path: Path, spec: DoqlSpec) -> None:
    """Parse a Makefile into :class:`Workflow` entries."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return

    seen: set[str] = {w.name for w in spec.workflows}

    for match in _TARGET_RE.finditer(content):
        name = match.group(1)
        deps_raw = match.group(2)
        body = match.group(3)

        if not _is_valid_target(name, deps_raw, seen):
            continue

        steps = _build_steps_from_body(body, deps_raw)
        workflow = _create_workflow(name, steps)
        if workflow:
            spec.workflows.append(workflow)
            seen.add(name)


def _parse_makefile_deps(deps_raw: str) -> list[str]:
    """Split the ``deps`` portion of ``target: dep1 dep2 ## comment``.

    Strips trailing ``## help`` comments and filters out dot-targets.
    """
    text = deps_raw.split("#", 1)[0]
    return [
        tok for tok in text.split()
        if tok and not tok.startswith(".")
    ]


def _build_taskfile_steps(task: dict[str, Any]) -> list[WorkflowStep]:
    """Build workflow steps from Taskfile task commands."""
    steps: list[WorkflowStep] = []
    for cmd in task.get("cmds") or []:
        if isinstance(cmd, str) and cmd.strip():
            steps.append(WorkflowStep(action="run", params={"cmd": cmd.strip()}))
    return steps


def _extract_taskfile_schedule(task: dict[str, Any]) -> str | None:
    """Extract schedule from Taskfile task if present."""
    schedule = task.get("schedule")
    return schedule if isinstance(schedule, str) else None


def _build_workflow_from_task(task_name: str, task: dict[str, Any]) -> Workflow | None:
    """Build a Workflow from a Taskfile task dict, or return None if no steps/schedule."""
    steps = _build_taskfile_steps(task)
    schedule = _extract_taskfile_schedule(task)
    if not steps and not schedule:
        return None
    return Workflow(
        name=str(task_name),
        trigger="schedule" if schedule else "manual",
        schedule=schedule,
        steps=steps,
    )


def _extract_taskfile_workflows(path: Path, spec: DoqlSpec) -> None:
    """Parse a Taskfile.yml into :class:`Workflow` entries."""
    data = load_yaml(path)
    if not data:
        return
    tasks = data.get("tasks") or {}
    if not isinstance(tasks, dict):
        return

    seen: set[str] = {w.name for w in spec.workflows}
    for task_name, task in tasks.items():
        if not isinstance(task, dict) or task_name in seen:
            continue
        wf = _build_workflow_from_task(task_name, task)
        if wf is not None:
            spec.workflows.append(wf)
            seen.add(str(task_name))


_CLICK_CMD_RE = re.compile(
    r'@\w+\.command(?:\([^)]*\))?[\r\n]+(?:[^\r\n]*[\r\n]+)*?def\s+([a-z_][a-z0-9_]*)',
    re.MULTILINE | re.IGNORECASE,
)

_INTERNAL_CMD_NAMES = {"main", "cli", "run", "start"}


def _find_cli_candidates(root: Path) -> list[Path]:
    """Return deduplicated list of CLI Python file candidates under *root*."""
    candidates: list[Path] = []
    for pattern in ["cli.py", "cli/*.py", "commands/*.py", "cmd/*.py"]:
        if "*" in pattern:
            parent, _ = pattern.split("/*")
            if (root / parent).is_dir():
                candidates.extend(walk_files(root / parent, extensions=(".py",)))
        else:
            if (root / pattern).exists():
                candidates.append(root / pattern)
    for pkg_dir in root.iterdir():
        if pkg_dir.is_dir() and not pkg_dir.name.startswith((".", "_")):
            cli_file = pkg_dir / "cli.py"
            if cli_file.exists():
                candidates.append(cli_file)
    return list(set(candidates))


def _detect_cli_command_name(root: Path) -> str:
    """Return the CLI entry-point name from pyproject.toml, or the directory name."""
    pyproj = root / "pyproject.toml"
    if pyproj.exists():
        try:
            with open(pyproj, "rb") as f:
                data = tomllib.load(f)
            for name in data.get("project", {}).get("scripts", {}).keys():
                if name not in ("api", "server"):
                    return str(name)
        except Exception:
            pass
    return root.name


def _build_workflow_steps(cmd_name: str, cli_command: str) -> list[WorkflowStep]:
    """Build WorkflowStep list for a detected CLI command."""
    if cmd_name == "analyze":
        tools = _CLI_WORKFLOW_COMMANDS[cmd_name].get("tools", "")
        return [
            WorkflowStep(action="run", params={"cmd": 'echo "🔬 Running project analysis..."'}),
            WorkflowStep(action="run", params={"cmd": f"{cli_command} analyze . --tools {tools}"}),
        ]
    return [WorkflowStep(action="run", params={"cmd": f"{cli_command} {cmd_name}"})]


def _scan_cli_file_for_workflows(
    cli_file: Path, cli_command: str, seen: set[str], spec: DoqlSpec,
) -> None:
    """Scan one CLI file and append discovered workflows to *spec*."""
    try:
        content = cli_file.read_text(encoding="utf-8")
    except OSError:
        return
    if "click" not in content.lower():
        return
    for match in _CLICK_CMD_RE.finditer(content):
        cmd_name = match.group(1)
        if cmd_name in _INTERNAL_CMD_NAMES or cmd_name in seen:
            continue
        if cmd_name not in _CLI_WORKFLOW_COMMANDS:
            continue
        steps = _build_workflow_steps(cmd_name, cli_command)
        spec.workflows.append(Workflow(name=cmd_name, trigger="manual", steps=steps))
        seen.add(cmd_name)


def _extract_python_cli_workflows(root: Path, spec: DoqlSpec) -> None:
    """Scan Python CLI source files for click commands and create workflows.

    Detects commands like 'analyze', 'test', 'build' from CLI modules and
    creates corresponding workflow definitions that run these commands.
    """
    seen: set[str] = {w.name for w in spec.workflows}
    cli_command = _detect_cli_command_name(root)
    for cli_file in _find_cli_candidates(root):
        _scan_cli_file_for_workflows(cli_file, cli_command, seen, spec)
