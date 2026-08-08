"""Tests for generated CI installation behavior."""
from __future__ import annotations

from doql.generators import ci_gen
from doql.parsers.models import DoqlSpec


def test_repository_containing_doql_source_installs_editable_package(tmp_path) -> None:
    (tmp_path / "doql").mkdir()
    (tmp_path / "doql" / "__init__.py").touch()

    ci_gen.generate(DoqlSpec(), {}, tmp_path)

    workflow = (tmp_path / ".github" / "workflows" / "doql-ci.yml").read_text()
    assert workflow.count("pip install -e .") == 3
    assert "pip install doql" not in workflow


def test_generated_application_installs_released_doql_package(tmp_path) -> None:
    ci_gen.generate(DoqlSpec(), {}, tmp_path)

    workflow = (tmp_path / ".github" / "workflows" / "doql-ci.yml").read_text()
    assert workflow.count("pip install doql") == 3
    assert "pip install -e ." not in workflow
