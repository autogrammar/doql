"""Versioned runtime contracts for the LLM-facing DOQL plan boundary."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

DOQL_PLAN_VERSION = "1.0.0"


def _contract_file(name: str):
    return files(__package__).joinpath("v1", name)


def load_schema() -> dict[str, Any]:
    """Load the packaged JSON Schema used at the model/runtime boundary."""
    return json.loads(_contract_file("doql-plan.schema.json").read_text(encoding="utf-8"))


def validate_payload(payload: object) -> None:
    """Fail closed when an LLM payload does not match DoqlPlan v1."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise RuntimeError("jsonschema not installed; pip install 'nlp2doql[llm]'") from exc

    validator = Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "$"
        raise ValueError(f"LLM response violates DoqlPlan v1 at {location}: {first.message}")


def response_format() -> dict[str, Any]:
    """Return LiteLLM/OpenAI structured-output configuration for this contract."""
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "doql_plan_v1",
            "strict": True,
            "schema": load_schema(),
        },
    }


__all__ = ["DOQL_PLAN_VERSION", "load_schema", "response_format", "validate_payload"]
