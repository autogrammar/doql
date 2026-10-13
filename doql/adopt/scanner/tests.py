"""TestQL scenario detection — *.testql.toon.yaml / *.testql.yaml imports."""
from __future__ import annotations

from pathlib import Path

from ...parsers.models import DoqlSpec

_SKIP_DIRS = {"venv", ".venv", "node_modules", "dist", "build", ".git", ".pytest_cache"}
_TESTQL_PATTERNS = ("*.testql.toon.yaml", "*.testql.yaml")


def _should_skip(path: Path) -> bool:
    return any(part in _SKIP_DIRS for part in path.parts)


def _common_import_glob(files: list[Path], root: Path, suffix: str) -> str:
    """Collapse discovered files into a single import glob when possible."""
    rel_dirs = sorted({f.parent.relative_to(root).as_posix() for f in files})
    if len(rel_dirs) == 1:
        base = rel_dirs[0]
        if base == ".":
            return f"*{suffix}"
        return f"{base}/**/*{suffix}"

    shared_prefix = list(Path(rel_dirs[0]).parts)
    for other in rel_dirs[1:]:
        parts_b = Path(other).parts
        matched: list[str] = []
        for a, b in zip(shared_prefix, parts_b):
            if a == b:
                matched.append(a)
            else:
                break
        shared_prefix = matched

    if shared_prefix:
        return f"{Path(*shared_prefix).as_posix()}/**/*{suffix}"
    return f"**/*{suffix}"


from .utils import walk_files


def scan_tests(root: Path, spec: DoqlSpec) -> None:
    """Detect TestQL files and populate spec.tests import globs."""
    toon_files: list[Path] = []
    yaml_files: list[Path] = []

    for path in walk_files(root, suffixes=(".testql.toon.yaml", ".testql.yaml")):
        if path.name.endswith(".testql.toon.yaml"):
            toon_files.append(path)
        else:
            yaml_files.append(path)

    if toon_files:
        spec.tests.append(
            _common_import_glob(toon_files, root, ".testql.toon.yaml")
        )
        # Add explicit imports for disjoint test trees (avoid one overly broad ** glob)
        rel_dirs = sorted({f.parent.relative_to(root).as_posix() for f in toon_files})
        if len(rel_dirs) > 1:
            broad = spec.tests[-1]
            if broad.startswith("**/"):
                spec.tests.pop()
                suffix = ".testql.toon.yaml"
                spec.tests.extend(
                    f"{d}/**/*{suffix}" for d in rel_dirs
                )
    if yaml_files:
        spec.tests.append(_common_import_glob(yaml_files, root, ".testql.yaml"))
