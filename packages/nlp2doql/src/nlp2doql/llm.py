"""Optional litellm planner for NL → DOQL."""

from __future__ import annotations

import json

from nlp2doql.contracts import DOQL_PLAN_VERSION, response_format, validate_payload
from nlp2doql.models import BlockPlan, DoqlPlan


def _parse_llm_json(text: str) -> dict:
    """Parse and validate the complete model response, without salvaging prose."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response must be a single JSON object") from exc
    if not isinstance(payload, dict):
        raise ValueError("LLM response must be a JSON object")
    validate_payload(payload)
    return payload


def plan_with_litellm(prompt: str, *, model: str) -> DoqlPlan:
    try:
        import litellm
    except ImportError as exc:
        raise RuntimeError("litellm not installed; pip install 'nlp2doql[llm]'") from exc

    system = (
        "You generate DOQL blocks in CSS-like LESS syntax. "
        f"Return only JSON conforming to the DoqlPlan {DOQL_PLAN_VERSION} contract. "
        'Use selectors like app, entity[name="X"], interface[type="web"], workflow[name="test"].'
    )
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        response_format=response_format(),
    )
    content = response.choices[0].message.content or ""
    payload = _parse_llm_json(content)
    blocks = [
        BlockPlan(
            selector=item["selector"],
            properties=item["properties"],
            comment=item.get("comment", ""),
        )
        for item in payload["blocks"]
    ]
    return DoqlPlan(
        title=payload["title"],
        blocks=blocks,
        planner="litellm",
        confidence=0.8,
        rationale=f"litellm model={model}",
        contract_version=payload["contractVersion"],
    )
