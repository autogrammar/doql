"""CLI: nlp2doql generate | validate | apply | edit | doctor."""

from __future__ import annotations

import argparse
import json
import shutil
import sys

from nlp2doql.apply import apply_nl, edit_nl
from nlp2doql.pipeline import generate_spec
from nlp2doql.validate import validate_doql_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Natural language control of DOQL manifests")
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate", help="Generate DOQL spec from NL")
    gen.add_argument("prompt", help="Natural language description")
    gen.add_argument("--out", "-o", help="Write .doql.less file path")
    gen.add_argument("--llm", action="store_true", help="Use SubLLM planner")
    gen.add_argument(
        "--model",
        default="openrouter/qwen/qwen3-coder-next",
        help="Ignored; SubLLM policy selects the model",
    )
    gen.add_argument("--validate", action="store_true", help="Validate via doql parser")
    gen.add_argument("--json", action="store_true", help="JSON output")

    val = sub.add_parser("validate", help="Validate existing DOQL file")
    val.add_argument("path", help="Path to .doql.less/.doql.css file")
    val.add_argument("--json", action="store_true")

    apply = sub.add_parser("apply", help="Apply NL control (query/patch/materialize/generate)")
    apply.add_argument("prompt", help="Natural language command")
    apply.add_argument("--file", help="Target DOQL manifest")
    apply.add_argument("--dest", help="Destination for materialize/generate")
    apply.add_argument("--with", dest="with_file", help="Content file for patch/append")
    apply.add_argument("--json", action="store_true")

    edit = sub.add_parser("edit", help="Edit DOQL block via NL + replacement content")
    edit.add_argument("prompt", help="Natural language edit intent")
    edit.add_argument("--file", help="Target DOQL manifest")
    edit.add_argument("--with", dest="with_file", required=True, help="Replacement block file")
    edit.add_argument("--json", action="store_true")

    doctor = sub.add_parser("doctor", help="Check doql dependency availability")
    doctor.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "doctor":
        status = {
            "doql": shutil.which("doql") is not None,
            "python_doql": False,
        }
        try:
            import doql  # noqa: F401

            status["python_doql"] = True
            status["doql_version"] = doql.__version__
        except ImportError:
            status["doql_version"] = None
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print(f"doql CLI: {'ok' if status['doql'] else 'missing'}")
            print(f"doql module: {'ok' if status['python_doql'] else 'missing'}")
            if status.get("doql_version"):
                print(f"doql version: {status['doql_version']}")
        return 0 if status["python_doql"] else 1

    if args.cmd == "validate":
        result = validate_doql_file(args.path)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("ok"):
                print("ok")
            else:
                for err in result.get("errors") or result.get("parse_errors") or []:
                    print(f"error: {err}", file=sys.stderr)
                if result.get("error"):
                    print(f"error: {result['error']}", file=sys.stderr)
        return 0 if result.get("ok") else 1

    if args.cmd == "apply":
        content = open(args.with_file, encoding="utf-8").read() if args.with_file else None
        result = apply_nl(args.prompt, file=args.file, content=content, dest=args.dest)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            if result.error:
                print(f"error: {result.error}", file=sys.stderr)
            if result.output:
                print(result.output.rstrip())
        return 0 if result.ok else 1

    if args.cmd == "edit":
        content = open(args.with_file, encoding="utf-8").read()
        result = edit_nl(args.prompt, file=args.file, content=content)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            if result.error:
                print(f"error: {result.error}", file=sys.stderr)
            if result.output:
                print(result.output.rstrip())
        return 0 if result.ok else 1

    if args.cmd == "generate":
        result = generate_spec(
            args.prompt,
            out_path=args.out,
            use_llm=args.llm,
            model=args.model,
            validate=args.validate,
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "ok": result.ok,
                        "doql": result.doql,
                        "planner": result.plan.planner,
                        "output_path": result.output_path,
                        "validation": result.validation,
                        "error": result.error,
                    },
                    indent=2,
                ),
            )
        else:
            if result.error:
                print(f"error: {result.error}", file=sys.stderr)
            if result.output_path:
                print(f"wrote: {result.output_path}")
            print(result.doql)
        return 0 if result.ok else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
