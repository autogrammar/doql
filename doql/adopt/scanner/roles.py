"""Role scanning — from env vars or SQL files."""
from __future__ import annotations

import re
from pathlib import Path

from ...parsers.models import DoqlSpec, Role
from .utils import walk_files


def _scan_sql_roles(root: Path, spec: DoqlSpec) -> None:
    """Detect roles from SQL files."""
    for sql in walk_files(root, extensions=(".sql",)):
        try:
            text = sql.read_text().lower()
        except Exception:
            continue
        if "role" not in text:
            continue
        for m in re.finditer(r"'(admin|user|editor|manager|operator|viewer)'", text):
            role_name = m.group(1)
            if not any(r.name == role_name for r in spec.roles):
                spec.roles.append(Role(name=role_name))


def scan_roles(root: Path, spec: DoqlSpec) -> None:
    """Detect roles from env vars or code patterns."""
    env_text = " ".join(spec.env_refs).upper()
    if "ADMIN" in env_text or "ROLE" in env_text:
        spec.roles.append(Role(name="admin", permissions=["*"]))
    _scan_sql_roles(root, spec)
