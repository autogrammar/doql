"""Runtime API tests — boot uvicorn, check /health and /openapi.json per example.

These tests require the runtime venv at /tmp/doql-runtime with:
  fastapi, uvicorn, sqlalchemy, pydantic, python-jose[cryptography],
  passlib[bcrypt], python-multipart.

Tests are automatically skipped when the runtime venv is absent or
when an example requires psycopg2 (postgres) and it isn't installed.
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import socket
import subprocess
import time
import urllib.request

import pytest

ROOT = pathlib.Path(__file__).parent.parent
EXAMPLES = ROOT / "examples"
_LOCAL_DOQL_BIN = ROOT / "venv" / "bin" / "doql"
DOQL_COMMAND = (str(_LOCAL_DOQL_BIN),) if _LOCAL_DOQL_BIN.exists() else ("doql",)
RUNTIME_VENV = pathlib.Path("/tmp/doql-runtime")
RUNTIME_PY = RUNTIME_VENV / "bin" / "python"
RUNTIME_UVICORN = RUNTIME_VENV / "bin" / "uvicorn"

# All examples that may produce an API
API_EXAMPLES = [
    "asset-management",
    "blog-cms",
    "calibration-lab",
    "crm-contacts",
    "e-commerce-shop",
    "iot-fleet",
    "notes-app",
    "todo-pwa",
]

skip_no_runtime = pytest.mark.skipif(
    not RUNTIME_UVICORN.exists(),
    reason=f"Runtime venv not found at {RUNTIME_VENV}",
)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _has_module(name: str) -> bool:
    py = str(RUNTIME_PY)
    try:
        r = subprocess.run([py, "-c", f"import {name}"],
                           capture_output=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False


@skip_no_runtime
@pytest.mark.parametrize("example", API_EXAMPLES)
def test_api_boot_and_health(example, tmp_path):
    """Build example, boot API, verify /health and /openapi.json."""
    src = EXAMPLES / example
    if not src.exists():
        pytest.skip(f"Example {example} not found")

    # Copy to tmp
    work = tmp_path / example
    shutil.copytree(src, work, ignore=shutil.ignore_patterns("build", ".github"))

    # Provide .env
    env_ex = work / ".env.example"
    if env_ex.exists() and not (work / ".env").exists():
        shutil.copy(env_ex, work / ".env")

    # Build
    result = subprocess.run(
        [*DOQL_COMMAND, "-d", str(work), "build", "--force"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, f"build failed: {result.stderr}"

    api_dir = work / "build" / "api"
    if not (api_dir / "main.py").exists():
        pytest.skip(f"{example}: no API generated")

    # Skip postgres-only examples when psycopg2 absent
    db_file = api_dir / "database.py"
    if db_file.exists():
        body = db_file.read_text()
        if "postgresql://" in body or "postgres://" in body:
            if not _has_module("psycopg2"):
                pytest.skip(f"{example}: needs psycopg2 for postgres")

    # Prepare data dir
    (api_dir / "data").mkdir(exist_ok=True)

    port = _free_port()
    env = os.environ.copy()
    env["JWT_SECRET"] = "test-secret"
    env["DATABASE_URL"] = f"sqlite:///./data/test-{port}.db"

    proc = subprocess.Popen(
        [str(RUNTIME_UVICORN), "main:app",
         "--host", "127.0.0.1", "--port", str(port)],
        cwd=api_dir, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )

    try:
        # Wait for server ready
        ok = False
        for _ in range(40):
            time.sleep(0.25)
            if proc.poll() is not None:
                out = proc.stdout.read().decode(errors="replace")
                pytest.fail(f"Server died (exit {proc.returncode}):\n{out[-500:]}")
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/health", timeout=1
                ) as resp:
                    if resp.status == 200:
                        ok = True
                        break
            except Exception:
                pass

        assert ok, "Server never became healthy within 10s"

        # Verify OpenAPI
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/openapi.json", timeout=2
        ) as resp:
            spec = json.loads(resp.read())
            endpoints = len(spec.get("paths", {}))
            assert endpoints > 0, "OpenAPI has 0 endpoints"

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── Static artifact checks (web, mobile, desktop, infra) ──────


FULL_STACK_EXAMPLES = [
    "asset-management",
    "blog-cms",
    "calibration-lab",
    "crm-contacts",
    "document-generator",
    "e-commerce-shop",
    "iot-fleet",
    "kiosk-station",
    "notes-app",
    "todo-pwa",
]


def _check_web_artifacts(web: pathlib.Path) -> None:
    if not web.exists() or not (web / "package.json").exists():
        return
    pkg = json.loads((web / "package.json").read_text())
    assert pkg.get("name"), "package.json missing name"
    assert (web / "vite.config.ts").exists(), "missing vite.config.ts"
    assert (web / "tsconfig.json").exists(), "missing tsconfig.json"
    assert (web / "index.html").exists(), "missing index.html"


def _check_mobile_artifacts(mobile: pathlib.Path) -> None:
    if not mobile.exists() or not (mobile / "manifest.json").exists():
        return
    manifest = json.loads((mobile / "manifest.json").read_text())
    assert manifest.get("name"), "manifest.json missing name"
    assert manifest.get("icons"), "manifest.json missing icons"
    assert (mobile / "service-worker.js").exists()
    sw = (mobile / "service-worker.js").read_text()
    assert "addEventListener" in sw, "service-worker.js invalid"
    assert (mobile / "app.js").exists()
    assert (mobile / "style.css").exists()


def _check_desktop_artifacts(desktop: pathlib.Path) -> None:
    if not desktop.exists() or not (desktop / "package.json").exists():
        return
    tauri = desktop / "src-tauri"
    assert tauri.is_dir(), "missing src-tauri/"
    tconf = tauri / "tauri.conf.json"
    assert tconf.exists(), "missing tauri.conf.json"
    data = json.loads(tconf.read_text())
    product = data.get("productName") or data.get("package", {}).get("productName")
    assert product, "tauri.conf.json missing productName"
    assert (tauri / "Cargo.toml").exists()
    main_rs = tauri / "src" / "main.rs"
    assert main_rs.exists()
    assert "tauri::Builder" in main_rs.read_text()


def _check_infra_artifacts(infra: pathlib.Path) -> None:
    if not infra.exists() or not (infra / "docker-compose.yml").exists():
        return
    import yaml
    compose = yaml.safe_load((infra / "docker-compose.yml").read_text())
    services = list((compose or {}).get("services", {}).keys())
    assert len(services) > 0, "docker-compose.yml has no services"
    dockerfile = infra / "Dockerfile"
    if dockerfile.exists():
        body = dockerfile.read_text()
        assert "FROM" in body, "Dockerfile missing FROM"


@pytest.mark.parametrize("example", FULL_STACK_EXAMPLES)
def test_build_produces_expected_targets(example, tmp_path):
    """Verify each example produces the correct set of build targets."""
    src = EXAMPLES / example
    if not src.exists():
        pytest.skip(f"Example {example} not found")

    work = tmp_path / example
    shutil.copytree(src, work, ignore=shutil.ignore_patterns("build", ".github"))

    env_ex = work / ".env.example"
    if env_ex.exists():
        shutil.copy(env_ex, work / ".env")

    result = subprocess.run(
        [*DOQL_COMMAND, "-d", str(work), "build", "--force"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, f"build failed: {result.stderr}"

    build = work / "build"
    _check_web_artifacts(build / "web")
    _check_mobile_artifacts(build / "mobile")
    _check_desktop_artifacts(build / "desktop")
    _check_infra_artifacts(build / "infra")
