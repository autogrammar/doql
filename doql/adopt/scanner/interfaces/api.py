"""Python API interface detection (FastAPI, Flask, Django)."""
from __future__ import annotations

import tomllib
from pathlib import Path

from ....parsers.models import DoqlSpec, Interface
from ..utils import walk_files


def _detect_framework_from_pyproject(pyproj: Path) -> str | None:
    """Detect web framework from pyproject.toml dependencies."""
    if not pyproj.exists():
        return None
    text = pyproj.read_text().lower()
    if "fastapi" in text:
        return "fastapi"
    if "flask" in text:
        return "flask"
    if "django" in text:
        return "django"
    return None


def _detect_framework_from_main_py(main_py: Path) -> str | None:
    """Detect web framework from main.py imports."""
    if not main_py.exists():
        return None
    try:
        text = main_py.read_text()
    except OSError:
        return None
    if "FastAPI" in text or "from fastapi" in text:
        return "fastapi"
    if "Flask" in text:
        return "flask"
    return None


def _detect_framework_from_any_py(root: Path) -> str | None:
    """Scan all Python files under root for FastAPI/Flask imports.

    Used as fallback when no api/main.py is found.
    """
    for py_file in walk_files(root, extensions=(".py",)):
        if "tests" in py_file.parts:
            continue
        try:
            text = py_file.read_text()
        except OSError:
            continue
        if "FastAPI" in text or "from fastapi" in text:
            return "fastapi"
        if "Flask" in text:
            return "flask"
    return None


def _find_api_main_file(root: Path) -> Path | None:
    """Find API main file in common locations."""
    api_dirs = ["api", "app", "src/api", "apps/api"]

    # Also check inside package directories (e.g. oqlos/api/main.py)
    for child in root.iterdir():
        if child.is_dir() and not child.name.startswith((".", "_")):
            if child.name not in ("venv", ".venv", "node_modules", "dist", "build", "tests"):
                api_dirs.append(f"{child.name}/api")

    for d in api_dirs:
        for fname in ("main.py", "app.py", "server.py"):
            candidate = root / d / fname
            if candidate.exists():
                return candidate
    return None


def _has_api_entry_point(pyproj: Path) -> bool:
    """Check if pyproject.toml has api/server entry point."""
    if not pyproj.exists():
        return False
    try:
        with open(pyproj, "rb") as f:
            data = tomllib.load(f)
        scripts = data.get("project", {}).get("scripts", {})
        for name in scripts.keys():
            if "server" in name or "api" in name:
                return True
    except Exception:
        pass
    return False


def _detect_api_auth(spec: DoqlSpec) -> str | None:
    """Detect authentication type from env vars."""
    for ref in spec.env_refs:
        if "JWT" in ref.upper() or "SECRET" in ref.upper():
            return "jwt"
    return None


def _detect_api_port(spec: DoqlSpec) -> str:
    """Detect API port from env vars."""
    for ref in spec.env_refs:
        if "PORT" in ref.upper() and "API" in ref.upper():
            return f"env.{ref}"
        if ref.upper() in ("PORT", "WEB_PORT", "SERVER_PORT"):
            return f"env.{ref}"
    return "8000"


def scan_python_api(root: Path, spec: DoqlSpec) -> None:
    """Detect Python API (FastAPI, Flask, Django).

    A project is considered to expose an API only when there is *evidence*
    of a serving entry point — not just a transitive dependency in
    ``pyproject.toml``. Evidence is one of:

    * an ``api/main.py`` / ``api/app.py`` (or ``<pkg>/api/main.py``) file,
    * a project script entry point whose name contains ``api``/``server``,
    * a top-level ``main.py`` that imports a known web framework.
    """
    pyproj = root / "pyproject.toml"
    framework_dep = _detect_framework_from_pyproject(pyproj)

    api_main = _find_api_main_file(root)
    has_entry_point = _has_api_entry_point(pyproj)
    main_py_framework = _detect_framework_from_main_py(root / "main.py")
    any_py_framework = _detect_framework_from_any_py(root)

    has_evidence = bool(api_main or has_entry_point or main_py_framework or any_py_framework)
    if not has_evidence:
        return

    framework = framework_dep or main_py_framework or any_py_framework or "fastapi"
    auth = _detect_api_auth(spec)

    iface = Interface(
        name="api",
        type="rest",
        framework=framework,
    )
    if auth:
        iface.auth = {"type": auth}
    spec.interfaces.append(iface)
