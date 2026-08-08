"""Offline parity and runtime tests for the LLM-facing DoqlPlan contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from nlp2doql.contracts import DOQL_PLAN_VERSION, load_schema, response_format, validate_payload
from nlp2doql.llm import _parse_llm_json
from nlp2doql.models import DoqlPlan

FIXTURES = Path(__file__).parent / "fixtures" / "contracts" / "v1"
CONTRACTS = Path(__file__).parents[1] / "src" / "nlp2doql" / "contracts" / "v1"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_fixture_is_accepted_by_runtime_contract() -> None:
    payload = _fixture("valid-doql-plan.json")
    validate_payload(payload)
    assert _parse_llm_json(json.dumps(payload)) == payload


@pytest.mark.parametrize(
    "payload",
    [
        _fixture("invalid-doql-plan.json"),
        {"contractVersion": "1.0.0", "title": "Missing blocks"},
        {
            "contractVersion": "1.0.0",
            "title": "Wrong property value",
            "blocks": [{"selector": "app", "properties": {"port": 8080}}],
        },
    ],
)
def test_invalid_payloads_fail_closed(payload: dict) -> None:
    with pytest.raises(ValueError, match="violates DoqlPlan v1"):
        validate_payload(payload)


def test_parser_rejects_prose_wrapped_json() -> None:
    with pytest.raises(ValueError, match="single JSON object"):
        _parse_llm_json('Here is the plan: {"contractVersion":"1.0.0"}')


def test_schema_runtime_and_dataclass_versions_match() -> None:
    schema = load_schema()
    assert schema["properties"]["contractVersion"]["const"] == DOQL_PLAN_VERSION
    assert DoqlPlan(title="test").contract_version == DOQL_PLAN_VERSION
    assert response_format()["json_schema"]["schema"] == schema


def test_protobuf_fields_and_gbnf_version_match_json_schema() -> None:
    proto = (CONTRACTS / "doql-plan.proto").read_text(encoding="utf-8")
    grammar = (CONTRACTS / "doql-plan.gbnf").read_text(encoding="utf-8")
    fields = set(re.findall(r"^  (?:repeated )?\w+(?:<[^>]+>)? (\w+) = \d+", proto, re.MULTILINE))
    assert {"contract_version", "title", "blocks", "selector", "properties", "comment"} <= fields
    assert f'\\"{DOQL_PLAN_VERSION}\\"' in grammar


def test_manifest_binds_every_artifact_to_runtime_boundary() -> None:
    manifest = json.loads((CONTRACTS / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == DOQL_PLAN_VERSION
    assert manifest["boundary"] == "nlp2doql.llm.plan_with_litellm"
    for artifact in manifest["artifacts"].values():
        assert (CONTRACTS / artifact).is_file()
