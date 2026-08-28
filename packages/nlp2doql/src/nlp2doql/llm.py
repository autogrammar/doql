"""Optional SubLLM planner for NL → DOQL."""

from __future__ import annotations

import json

from nlp2doql.contracts import DOQL_PLAN_VERSION, response_format, validate_payload
from nlp2doql.models import BlockPlan, DoqlPlan

try:
    from subllm import complete as subllm_complete
except ImportError:  # pragma: no cover - optional extra
    subllm_complete = None

SUBLLM_APPLICATION = "autogrammar-doql"
SUBLLM_FUNCTION = "translate"


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


def _plan_from_payload(payload: dict, *, rationale: str) -> DoqlPlan:
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
        planner="subllm",
        confidence=0.8,
        rationale=rationale,
        contract_version=payload["contractVersion"],
    )


def plan_with_subllm(prompt: str, *, model: str | None = None) -> DoqlPlan:
    """Plan DOQL through the central SubLLM route. ``model`` is ignored."""
    if subllm_complete is None:
        raise RuntimeError(
            "subactor-subllm is not installed; pip install 'nlp2doql[llm]'"
        )

    system = (
        "You generate DOQL blocks in CSS-like LESS syntax. "
        f"Return only JSON conforming to the DoqlPlan {DOQL_PLAN_VERSION} contract. "
        'Use selectors like app, entity[name="X"], interface[type="web"], workflow[name="test"].'
    )
    response = subllm_complete(
        SUBLLM_APPLICATION,
        SUBLLM_FUNCTION,
        [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        response_format=response_format(),
    )
    payload = _parse_llm_json(response.content or "")
    return _plan_from_payload(
        payload,
        rationale=f"subllm route={SUBLLM_APPLICATION}/{SUBLLM_FUNCTION}",
    )


def plan_with_litellm(prompt: str, *, model: str) -> DoqlPlan:
    """Compatibility alias; provider and model stay in SubLLM policy."""
    return plan_with_subllm(prompt, model=model)
