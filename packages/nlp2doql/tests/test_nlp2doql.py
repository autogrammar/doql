from pathlib import Path
from unittest.mock import MagicMock, patch

from nlp2doql import generate_spec
from nlp2doql.cli import main as cli_main
from nlp2doql.validate import validate_doql, validate_doql_file


def test_validate_doql_file_app_manifest() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    result = validate_doql_file(root / "app.doql.less")
    assert result.get("ok") is True
    assert result.get("app_name") == "doql"


def test_validate_doql_valid() -> None:
    source = """
    app {
      name: "My App";
    }
    entity[name="User"] {
      name: string;
    }
    """
    res = validate_doql(source)
    assert res.get("ok") is True
    assert res.get("app_name") == "My App"
    assert res.get("entity_count") == 1


def test_validate_doql_invalid() -> None:
    source = """
    invalid syntax {
    """
    res = validate_doql(source)
    assert res.get("ok") is False
    assert "error" in res or "parse_errors" in res


def test_generate_spec_rules() -> None:
    res = generate_spec("build crm app with contacts and install workflow")
    assert res.ok is True
    assert "Contact" in res.doql
    assert "install" in res.doql
    assert res.plan.planner == "rules"


@patch("litellm.completion")
def test_generate_spec_llm(mock_completion: MagicMock) -> None:
    # Mock litellm response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content='{"contractVersion": "1.0.0", "title": "CRM", "blocks": [{"selector": "app", "properties": {"name": "CRM"}}, {"selector": "entity[name=\\"Contact\\"]", "properties": {"first_name": "string"}}]}'
            )
        )
    ]
    mock_completion.return_value = mock_response

    res = generate_spec("create crm", use_llm=True, model="ollama/qwen2.5:7b")
    assert res.ok is True
    assert res.plan.planner == "litellm"
    assert res.plan.contract_version == "1.0.0"
    assert "Contact" in res.doql
    assert mock_completion.call_args.kwargs["response_format"]["type"] == "json_schema"


def test_cli_doctor() -> None:
    with patch("sys.stdout"):
        code = cli_main(["doctor"])
        assert code == 0


def test_cli_validate(tmp_path: Path) -> None:
    f = tmp_path / "app.doql.less"
    f.write_text('app { name: "Demo"; }', encoding="utf-8")
    code = cli_main(["validate", str(f)])
    assert code == 0


def test_cli_generate(tmp_path: Path) -> None:
    out = tmp_path / "app.doql.less"
    code = cli_main(["generate", "create crm", "--out", str(out)])
    assert code == 0
    assert out.is_file()
    assert "Contact" in out.read_text(encoding="utf-8")
