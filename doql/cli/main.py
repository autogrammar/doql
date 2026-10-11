"""Main entry point for doql CLI.

This module sets up the argument parser and dispatches to command handlers.
All actual command logic is in doql/cli/commands/.
"""
from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from typing import cast

from .. import __version__
from .commands import (
    cmd_adopt, cmd_build, cmd_doctor, cmd_drift, cmd_publish, cmd_init, cmd_validate,
    cmd_workflows,
    cmd_plan, cmd_run, cmd_sync, cmd_deploy,
    cmd_export, cmd_import, cmd_generate, cmd_render, cmd_query,
    cmd_topology,
    cmd_kiosk, cmd_quadlet, cmd_docs,
    register_workspace_parser,
)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser with all subcommands."""
    p = argparse.ArgumentParser(
        prog="doql",
        description="Declarative OQL — build apps from .doql files"
    )
    p.add_argument("--version", action="version", version=f"doql {__version__}")
    p.add_argument("-d", "--dir", help="Project directory (default: current)")
    p.add_argument("-f", "--file", help="Doql file (default: app.doql)")
    
    sub = p.add_subparsers(dest="cmd", required=True)
    
    # init
    s = sub.add_parser("init", help="Create new project from template")
    s.add_argument("name", help="Project name / directory (use '-' with --list to just list)")
    s.add_argument("--template", "-t", help="Template name — use --list-templates to see all")
    s.add_argument("--list-templates", action="store_true", help="List available templates and exit")
    s.set_defaults(func=cmd_init)
    
    # validate
    s = sub.add_parser("validate", help="Validate .doql + .env")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("workflows", help="Print declared workflows and dependencies (no device scan)")
    s.add_argument("--format", choices=("text", "json"), default="text")
    s.set_defaults(func=cmd_workflows)
    
    # plan
    s = sub.add_parser("plan", help="Dry-run: show what would be generated")
    s.set_defaults(func=cmd_plan)
    
    # build
    s = sub.add_parser("build", help="Generate all code")
    s.add_argument("--force", action="store_true")
    s.add_argument("--no-overwrite", action="store_true",
                   help="Skip files that already exist (merge-friendly)")
    s.add_argument("--from-device", dest="from_device", metavar="USER@HOST",
                   help="Scan a live device first, then build from the resulting "
                        "app.doql.less (requires doql[device-adopt])")
    s.add_argument("--ssh-key", dest="ssh_key",
                   help="Path to SSH private key for --from-device")
    s.add_argument("--layers", action="append", default=None,
                   help="Op3 layer ids to probe (repeatable). Only used with "
                        "--from-device; see `doql adopt --help` for defaults")
    s.add_argument("--watch", action="store_true",
                   help="Watch .doql file and rebuild on changes (requires watchfiles or watchdog)")
    s.set_defaults(func=cmd_build)
    
    # run
    s = sub.add_parser("run", help="Run locally (dev mode)")
    s.add_argument("--target", "-t", choices=["api", "web", "mobile", "desktop"],
                   help="Run a specific target (default: full stack via docker-compose)")
    s.add_argument("-f", "--file", dest="file",
                   help="Doql file — build on-the-fly into .doql/ and run")
    s.add_argument("--port", "-p", type=int,
                   help="Port override (default: api=8000, web=5173, mobile=8091)")
    s.set_defaults(func=cmd_run)
    
    # deploy
    s = sub.add_parser("deploy", help="Deploy to environment")
    s.add_argument("--env", choices=["dev", "staging", "prod"])
    s.set_defaults(func=cmd_deploy)
    
    # sync
    s = sub.add_parser("sync", help="Re-generate changed parts (merge-friendly)")
    s.set_defaults(func=cmd_sync)
    
    # export
    s = sub.add_parser("export", help="Export OpenAPI / Postman / TS SDK / YAML / Markdown / CSS / LESS / SASS")
    s.add_argument("--format", required=True,
                   choices=["openapi", "postman", "typescript-sdk",
                            "yaml", "markdown", "css", "less", "sass"])
    s.add_argument("-o", "--output", help="Output file path (default: stdout)")
    s.set_defaults(func=cmd_export)

    # import
    s = sub.add_parser("import", help="Import YAML → DOQL format")
    s.add_argument("source", help="Source YAML file path")
    s.add_argument("--format", required=True,
                   choices=["yaml", "css", "less", "sass"],
                   help="Output format")
    s.add_argument("-o", "--output", help="Output file path")
    s.set_defaults(func=cmd_import)
    
    # generate
    s = sub.add_parser("generate", help="Generate a single document/artifact")
    s.add_argument("artifact", help="Artifact name (must match DOCUMENT in .doql)")
    s.set_defaults(func=cmd_generate)
    
    # render
    s = sub.add_parser("render", help="Render a template with data")
    s.add_argument("template", help="Template file path")
    s.set_defaults(func=cmd_render)
    
    # query
    s = sub.add_parser("query", help="Query a DATA source → JSON")
    s.add_argument("data", help="DATA source name")
    s.set_defaults(func=cmd_query)

    # topology
    s = sub.add_parser("topology", help="Emit canonical site topology as JSON")
    s.add_argument("--main-domain", help="Mark the subscription's main domain")
    s.set_defaults(func=cmd_topology)
    
    # kiosk
    s = sub.add_parser("kiosk", help="Kiosk appliance management")
    s.add_argument("--install", action="store_true", help="Install kiosk on this device")
    s.set_defaults(func=cmd_kiosk)
    
    # quadlet
    s = sub.add_parser("quadlet", help="Podman Quadlet management")
    s.add_argument("--install", action="store_true", help="Install Quadlet to systemd")
    s.set_defaults(func=cmd_quadlet)
    
    # docs
    s = sub.add_parser("docs", help="Generate documentation site")
    s.set_defaults(func=cmd_docs)

    # adopt
    s = sub.add_parser("adopt", help="Reverse-engineer existing project → app.doql.css/.less/.sass")
    s.add_argument("target", nargs="?",
                   help="Project directory to scan (omit with --from-device)")
    s.add_argument("-o", "--output", help="Output filename (default: app.doql.{fmt})")
    s.add_argument("-f", "--format", choices=["css", "less", "sass"], default="less",
                   help="Output format (default: less)")
    s.add_argument("--force", action="store_true", help="Overwrite existing file")
    s.add_argument("--recursive", action="store_true",
                   help="Discover sub-projects and generate per-folder manifests + root with project blocks")
    s.add_argument("--from-device", dest="from_device", metavar="USER@HOST",
                   help="Scan a live device via SSH using op3 (requires doql[device-adopt])")
    s.add_argument("--ssh-key", dest="ssh_key",
                   help="Path to SSH private key for --from-device")
    s.add_argument("--layers", action="append", default=None,
                   help="Op3 layer ids to probe (repeatable). Defaults to runtime + "
                        "services + endpoints + business.health")
    s.set_defaults(func=cmd_adopt)

    # doctor
    s = sub.add_parser("doctor", help="Project health check & diagnostics")
    s.add_argument("--env", help="Run remote diagnostics for named environment")
    s.add_argument("--fix", action="store_true", help="Apply automatic fixes for warnings")
    s.set_defaults(func=cmd_doctor)

    # drift
    s = sub.add_parser("drift",
                       help="Compare declared state (app.doql.less) vs. a live device scan")
    s.add_argument("--from-device", dest="from_device", metavar="USER@HOST", required=True,
                   help="SSH target to scan (required; uses op3 — install doql[device-adopt])")
    s.add_argument("--file", dest="file",
                   help="Path to intended-state file (default: app.doql.less in CWD)")
    s.add_argument("--ssh-key", dest="ssh_key",
                   help="Path to SSH private key")
    s.add_argument("--layers", action="append", default=None,
                   help="Op3 layer ids to probe (repeatable). Defaults to runtime + "
                        "services + endpoints + business.health")
    s.add_argument("--json", action="store_true",
                   help="Emit a machine-readable JSON report instead of the table view")
    s.set_defaults(func=cmd_drift)

    # publish
    s = sub.add_parser("publish", help="Publish artifacts (PyPI, npm, Docker, GitHub)")
    s.add_argument("--target", "-t",
                   help="Comma-separated targets: pypi,npm,docker,github (default: all)")
    s.add_argument("--dry-run", action="store_true", help="Simulate without publishing")
    s.set_defaults(func=cmd_publish)

    # workspace — multi-project operations
    register_workspace_parser(sub)

    return p


def main() -> int:
    """Main entry point for doql CLI.
    
    Parses arguments and dispatches to the appropriate command handler.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        from ..autoupdate import check_for_updates
        check_for_updates("doql")
    except Exception:
        pass

    p = create_parser()
    args = p.parse_args()
    handler = cast(Callable[[argparse.Namespace], int], args.func)
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
