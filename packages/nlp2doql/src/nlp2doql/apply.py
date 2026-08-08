"""Apply natural-language DOQL control via nlp2uri + uri2doql."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from uri2doql.nlp2uri import best_uri


@dataclass
class ApplyResult:
    ok: bool
    prompt: str
    action: str = ""
    uri: str = ""
    output: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "prompt": self.prompt,
            "action": self.action,
            "uri": self.uri,
            "output": self.output,
            "data": self.data,
            "error": self.error,
        }


def _intent(prompt: str) -> str:
    text = prompt.lower()
    if any(w in text for w in ("validate", "waliduj", "sprawdź", "sprawdz")):
        return "validate"
    if any(w in text for w in ("generate", "wygeneruj", "stwórz", "stworz", "create", "build")):
        return "generate"
    if any(w in text for w in ("patch", "update", "zmień", "zmien", "edytuj", "edit", "replace")):
        return "patch"
    if any(w in text for w in ("append", "dodaj", "add block")):
        return "append"
    if any(w in text for w in ("materialize", "zapisz", "export", "write")):
        return "materialize"
    if any(w in text for w in ("query", "pokaż", "pokaz", "read", "show", "get")):
        return "query"
    return "query"


def apply_nl(
    prompt: str,
    *,
    file: str | None = None,
    content: str | None = None,
    dest: str | None = None,
) -> ApplyResult:
    """Resolve NL to URI/intent and execute DOQL control action."""
    intent = _intent(prompt)
    path_match = re.search(r"([\w./-]+\.doql(?:\.(?:less|css|sass))?)", prompt, re.IGNORECASE)
    explicit_file = path_match.group(1) if path_match else file

    try:
        if intent == "validate":
            from nlp2doql.validate import validate_doql_file

            target = explicit_file or "app.doql.less"
            result = validate_doql_file(target)
            return ApplyResult(
                ok=bool(result.get("ok")),
                prompt=prompt,
                action="validate",
                output=json.dumps(result, ensure_ascii=False, indent=2),
                data=result,
                error=None
                if result.get("ok")
                else str(result.get("errors") or result.get("error")),
            )

        if intent == "generate":
            from nlp2doql.pipeline import generate_spec

            generated = generate_spec(prompt, out_path=dest or explicit_file, validate=True)
            return ApplyResult(
                ok=generated.ok,
                prompt=prompt,
                action="generate",
                uri="doql://generate",
                output=generated.doql,
                data={
                    "output_path": generated.output_path,
                    "planner": generated.plan.planner,
                    "validation": generated.validation,
                },
                error=generated.error,
            )

        hit = best_uri(prompt, file=explicit_file, dest=dest)
        if not hit:
            return ApplyResult(
                ok=False, prompt=prompt, action=intent, error="could not resolve NL to doql:// URI"
            )

        uri = hit.uri
        if intent in {"patch", "update", "append"}:
            if not content:
                return ApplyResult(
                    ok=False,
                    prompt=prompt,
                    action=intent,
                    uri=uri,
                    error="patch/edit requires content (use --with or content=)",
                )
            from uri2doql.patch import apply_uri

            mode = "append" if intent == "append" else "patch"
            result = apply_uri(uri, content=content, file=explicit_file, mode=mode)
            return ApplyResult(
                ok=result.ok,
                prompt=prompt,
                action=intent,
                uri=uri,
                output=json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
                data=result.to_dict(),
                error=result.error,
            )

        if intent == "materialize":
            from uri2doql.materialize import materialize_uri

            result = materialize_uri(uri, dest=dest)
            return ApplyResult(
                ok=result.ok,
                prompt=prompt,
                action="materialize",
                uri=uri,
                output=json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
                data=result.to_dict(),
                error=result.error,
            )

        from uri2doql.query import query_uri

        query = query_uri(
            uri, file=explicit_file, fmt="less" if "less" in prompt.lower() else "json"
        )
        return ApplyResult(
            ok=query.ok,
            prompt=prompt,
            action="query",
            uri=uri,
            output=query.rendered or json.dumps(query.data, ensure_ascii=False, indent=2),
            data=query.to_dict(),
            error=query.error,
        )
    except Exception as exc:
        return ApplyResult(ok=False, prompt=prompt, action=intent, error=str(exc))


def edit_nl(
    prompt: str,
    *,
    file: str | None = None,
    content: str,
) -> ApplyResult:
    """Edit DOQL via NL prompt + replacement block content."""
    return apply_nl(prompt, file=file, content=content)
