"""Tests for nlp2doql rules and pipeline."""

from nlp2doql.pipeline import generate_spec
from nlp2doql.rules import plan_with_rules


def test_plan_crm_entities():
    plan = plan_with_rules("CRM with contacts and deals")
    selectors = [block.selector for block in plan.blocks]
    assert "app" in selectors
    assert 'entity[name="Contact"]' in selectors
    assert 'interface[type="api"]' in selectors


def test_generate_and_validate_todo():
    result = generate_spec("todo PWA with tasks", validate=True)
    assert result.ok
    assert 'entity[name="Todo"]' in result.doql
    assert result.validation is not None
    assert result.validation["ok"]


def test_generate_writes_file(tmp_path):
    out = tmp_path / "app.doql.less"
    result = generate_spec("simple API backend", out_path=out)
    assert result.ok
    assert out.is_file()
    assert 'interface[type="api"]' in out.read_text(encoding="utf-8")
