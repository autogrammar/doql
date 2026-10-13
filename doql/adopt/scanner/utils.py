"""Utility functions for project scanning."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, cast


def load_yaml(path: Path) -> dict[str, Any] | None:
    """Safely load a YAML file."""
    try:
        import yaml  # type: ignore[import-untyped]
        data: Any = yaml.safe_load(path.read_text()) or {}
        if not isinstance(data, dict) or not all(isinstance(key, str) for key in data):
            return None
        return cast(dict[str, Any], data)
    except Exception:
        return None


def find_compose(root: Path) -> Path | None:
    """Find docker-compose file."""
    candidates = [
        root / "docker-compose.yml",
        root / "docker-compose.yaml",
        root / "infra" / "docker-compose.yml",
        root / "infra" / "docker" / "prod" / "docker-compose.prod.yml",
        root / "infra" / "docker" / "dev" / "docker-compose.dev.yml",
        root / "docker" / "docker-compose.yml",
        root / "docker" / "docker-compose.dev.yml",
        root / "docker" / "docker-compose.prod.yml",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


_DEFAULT_SKIP_DIRS: frozenset[str] = frozenset({
    "venv",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".git",
    ".pytest_cache",
    ".cache",
    ".tox",
    ".mypy_cache",
    ".ruff_cache",
    "c2004",
    "c2004-git-backup",
    "workshop",
    "managed_components",
    "vendor",
    ".subactor",
    ".worktrees",
    ".planfile",
})


def should_skip_dir(dirname: str, extra_skips: frozenset[str] | set[str] | None = None) -> bool:
    lower = dirname.lower()
    if lower.startswith("."):
        return True
    if lower in _DEFAULT_SKIP_DIRS:
        return True
    if extra_skips and lower in extra_skips:
        return True
    return False


def walk_files(
    root: Path,
    extensions: tuple[str, ...] | None = None,
    suffixes: tuple[str, ...] | None = None,
    prefixes: tuple[str, ...] | None = None,
    skip_dirs: frozenset[str] = _DEFAULT_SKIP_DIRS,
) -> list[Path]:
    """Pruned directory traversal avoiding expensive recursion into ignored trees."""
    results: list[Path] = []
    if not root.is_dir():
        return results

    import os
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d, skip_dirs)]
        p_dir = Path(dirpath)
        for fn in filenames:
            if extensions and not any(fn.endswith(ext) for ext in extensions):
                continue
            if suffixes and not any(fn.endswith(suf) for suf in suffixes):
                continue
            if prefixes and not any(fn.startswith(pre) for pre in prefixes):
                continue
            results.append(p_dir / fn)
    return results


def find_dockerfiles(root: Path) -> list[Path]:
    """Find all Dockerfiles."""
    return walk_files(root, prefixes=("Dockerfile",))


def camel_to_kebab(name: str) -> str:
    """Convert CamelCase/PascalCase to kebab-case."""
    name = name.removesuffix("Page").removesuffix("View")
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def snake_to_pascal(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(w.capitalize() for w in name.split("_"))


def normalize_python_type(t: str) -> str:
    """Normalize Python type annotations to DOQL types."""
    t = t.strip()
    t = re.sub(r'Optional\[(.+)\]', r'\1', t)
    mapping = {
        "str": "string", "int": "int", "float": "float",
        "bool": "bool", "datetime": "datetime", "date": "date",
        "UUID": "uuid", "uuid": "uuid", "dict": "json",
        "list": "json", "List": "json", "Dict": "json",
        "Any": "json",
    }
    return mapping.get(t, t)


def normalize_sqlalchemy_type(t: str) -> str:
    """Normalize SQLAlchemy Column types to DOQL types."""
    mapping = {
        "String": "string", "Integer": "int", "Float": "float",
        "Boolean": "bool", "DateTime": "datetime", "Date": "date",
        "Text": "text", "JSON": "json", "UUID": "uuid",
    }
    return mapping.get(t, t.lower())


# SQL type pattern mappings: (substring, doql_type)
_SQL_TYPE_PATTERNS: list[tuple[tuple[str, ...], str]] = [
    (("VARCHAR", "TEXT", "CHAR"), "string"),
    (("INT",), "int"),
    (("FLOAT", "REAL", "DOUBLE", "NUMERIC"), "float"),
    (("BOOL",), "bool"),
    (("DATE", "TIME"), "datetime"),
    (("UUID",), "uuid"),
    (("JSON",), "json"),
    (("BLOB", "BYTE"), "binary"),
]


def normalize_sql_type(t: str) -> str:
    """Normalize SQL column types to DOQL types using pattern matching."""
    t_upper = t.upper()
    for patterns, doql_type in _SQL_TYPE_PATTERNS:
        if any(p in t_upper for p in patterns):
            return doql_type
    return t.lower()
