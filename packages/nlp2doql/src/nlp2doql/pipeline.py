"""End-to-end NL → DOQL generation pipeline."""

from __future__ import annotations

from pathlib import Path

from nlp2doql.models import GenerateResult
from nlp2doql.rules import plan_with_rules
from nlp2doql.validate import validate_doql


def generate_spec(
    prompt: str,
    *,
    out_path: str | Path | None = None,
    use_llm: bool = False,
    model: str = "openrouter/qwen/qwen3-coder-next",
    validate: bool = False,
) -> GenerateResult:
    """Plan and render DOQL LESS from natural language."""
    try:
        if use_llm:
            from nlp2doql.llm import plan_with_subllm

            plan = plan_with_subllm(prompt, model=model)
        else:
            plan = plan_with_rules(prompt)
        doql = plan.to_doql_less()
    except Exception as exc:
        return GenerateResult(
            ok=False,
            doql="",
            plan=plan_with_rules(prompt),
            error=str(exc),
        )

    validation = validate_doql(doql) if validate else None

    output_path = None
    if out_path is not None:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(doql, encoding="utf-8")
        output_path = str(path.resolve())

    ok = True
    if validation is not None and not validation.get("ok", False):
        ok = False

    return GenerateResult(
        ok=ok,
        doql=doql,
        plan=plan,
        validation=validation,
        output_path=output_path,
    )
