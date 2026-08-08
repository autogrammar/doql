"""Regression tests for generated TypeScript property access."""
from __future__ import annotations

from doql.generators.web_gen.pages import _gen_entity_page
from doql.parsers.models import Entity, EntityField


def test_entity_fields_with_punctuation_use_quoted_typescript_properties() -> None:
    entity = Entity(
        name="Device",
        fields=[EntityField(name="when-device_type", type="string")],
    )

    generated = _gen_entity_page(entity)

    assert '"when-device_type": any' in generated
    assert 'form["when-device_type"]' in generated
    assert '["when-device_type"]: e.target.value' in generated
    assert 'item["when-device_type"]' in generated
    assert "form.when-device_type" not in generated
