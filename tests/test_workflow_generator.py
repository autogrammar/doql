"""Regression tests for generated workflow Python identifiers."""
from __future__ import annotations

import py_compile

from doql.generators import workflow_gen
from doql.parsers.models import DoqlSpec, Workflow, WorkflowStep


def test_workflow_names_with_punctuation_generate_valid_python(tmp_path) -> None:
    spec = DoqlSpec(
        workflows=[
            Workflow(
                name="deps:update",
                schedule='schedule "0 8 * * *"',
                steps=[WorkflowStep(action="deps.update")],
            ),
            Workflow(name="42-release", steps=[WorkflowStep(action="release")]),
        ]
    )

    workflow_gen.generate(spec, {}, tmp_path)

    assert (tmp_path / "wf_deps_update.py").is_file()
    assert (tmp_path / "wf_workflow_42_release.py").is_file()
    for generated in tmp_path.glob("*.py"):
        py_compile.compile(str(generated), doraise=True)
