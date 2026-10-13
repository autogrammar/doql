"""Environment scanning — .env files and docker-compose variants."""
from __future__ import annotations

import re
from pathlib import Path

from ...parsers.models import DoqlSpec, Environment
from .utils import find_compose, load_yaml, walk_files

_SOURCE_ENV_RE = re.compile(
    r'(?:os\.getenv|os\.environ\.get|os\.environ)\(\s*["\']([A-Z][A-Z0-9_]*)["\']'
)
_PROFILE_PREFIXES = {
    "SMTP": "profile_smtp",
    "NLP2ENV": "runtime_nlp2env",
    "PFIX": "runtime_pfix",
    "OLLAMA": "runtime_ollama",
    "OPENROUTER": "runtime_llm",
}


def _detect_local_env(root: Path, spec: DoqlSpec) -> None:
    """Detect local environment from .env / .env.example."""
    local_env = Environment(name="local")
    env_path = root / ".env"
    example_path = root / ".env.example"

    keys: list[str] = []
    if env_path.exists():
        local_env.env_file = ".env"
        keys.extend(_extract_env_refs(env_path, spec))
    if example_path.exists():
        local_env.config["template_file"] = ".env.example"
        example_keys = _extract_env_refs(example_path, spec, merge=True)
        keys.extend(k for k in example_keys if k not in keys)
        if not local_env.env_file:
            local_env.env_file = ".env.example"

    if spec.python_requires:
        local_env.config["python_version"] = spec.python_requires
    if keys:
        local_env.config["vars"] = ", ".join(sorted(set(keys)))
    spec.environments.append(local_env)


def _extract_env_refs(
    env_path: Path,
    spec: DoqlSpec,
    *,
    merge: bool = False,
) -> list[str]:
    """Extract environment variable keys from a dotenv file."""
    found: list[str] = []
    try:
        text = env_path.read_text(errors="ignore")
    except OSError:
        return found
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key = line.split("=", 1)[0].strip()
            if not key:
                continue
            found.append(key)
            if key not in spec.env_refs:
                spec.env_refs.append(key)
            elif not merge:
                continue
    return found


def _scan_source_env_refs(root: Path, spec: DoqlSpec) -> None:
    """Collect getenv / os.environ keys referenced in Python source."""
    src = root / "src"
    if not src.is_dir():
        return
    for py_file in walk_files(src, extensions=(".py",)):
        try:
            text = py_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for key in _SOURCE_ENV_RE.findall(text):
            if key not in spec.env_refs:
                spec.env_refs.append(key)


def _attach_env_profiles(env: Environment, env_refs: list[str]) -> None:
    """Group known env key prefixes into profile hints on the environment block."""
    grouped: dict[str, list[str]] = {}
    for key in env_refs:
        for prefix, profile_name in _PROFILE_PREFIXES.items():
            if key.startswith(prefix):
                grouped.setdefault(profile_name, []).append(key)
                break
    for profile_name, keys in sorted(grouped.items()):
        env.config[profile_name] = ", ".join(sorted(set(keys)))


def _detect_env_files(root: Path, spec: DoqlSpec) -> None:
    """Detect staging/prod environments from .env.* files."""
    skip_names = {"example", "local", "docker", "test", "bak"}
    for env_file in sorted(root.glob(".env.*")):
        name = env_file.name.split(".", 2)[-1]
        if name in skip_names:
            continue
        env = Environment(name=name, env_file=env_file.name)
        keys = _extract_env_refs(env_file, spec)
        if keys:
            env.config["vars"] = ", ".join(sorted(set(keys)))
        _attach_env_profiles(env, keys)
        _assign_ssh_host(env, name, spec.env_refs)
        spec.environments.append(env)


def _assign_ssh_host(env: Environment, name: str, env_refs: list[str]) -> None:
    """Assign ssh_host from env refs matching the environment name."""
    for ref in env_refs:
        if name.upper() in ref.upper() and "HOST" in ref.upper():
            env.ssh_host = f"env.{ref}"
            return


# Path patterns for docker-compose environment detection
_COMPOSE_PATTERNS: list[tuple[str, list[str]]] = [
    ("dev", ["docker-compose.dev.yml", "docker/docker-compose.dev.yml",
              "infra/docker/dev/docker-compose.dev.yml"]),
    ("staging", ["docker-compose.staging.yml", "docker/docker-compose.staging.yml"]),
    ("prod", ["docker-compose.prod.yml", "docker/docker-compose.prod.yml",
               "infra/docker/prod/docker-compose.prod.yml"]),
]


def _detect_compose_envs(root: Path, spec: DoqlSpec) -> None:
    """Detect environments from docker-compose variant files."""
    existing_names = {e.name for e in spec.environments}
    for env_name, paths in _COMPOSE_PATTERNS:
        if env_name in existing_names:
            continue
        for p in paths:
            if (root / p).exists():
                env = Environment(name=env_name, runtime="docker-compose")
                env_file = root / f".env.{env_name}"
                if env_file.exists():
                    env.env_file = env_file.name
                    keys = _extract_env_refs(env_file, spec)
                    if keys:
                        env.config["vars"] = ", ".join(sorted(set(keys)))
                spec.environments.append(env)
                break


def finalize_environment_runtimes(root: Path, spec: DoqlSpec) -> None:
    """Set sensible runtime after deploy target is known."""
    deploy_target = spec.deploy.target if spec.deploy else ""
    compose_file = spec.deploy.config.get("compose_file") if spec.deploy else None
    for env in spec.environments:
        if compose_file and env.name in {"dev", "staging", "prod"}:
            env.runtime = "docker-compose"
            continue
        if deploy_target in {"pip", "makefile"} and not compose_file:
            env.runtime = "python"
        elif deploy_target == "docker-compose":
            env.runtime = "docker-compose"
        elif not env.runtime:
            env.runtime = deploy_target or "local"


def scan_environments(root: Path, spec: DoqlSpec) -> None:
    """Detect environments from .env files and docker-compose variants."""
    _detect_local_env(root, spec)
    _detect_env_files(root, spec)
    _detect_compose_envs(root, spec)
    _scan_source_env_refs(root, spec)
    local = next((env for env in spec.environments if env.name == "local"), None)
    if local is not None:
        _attach_env_profiles(local, spec.env_refs)
