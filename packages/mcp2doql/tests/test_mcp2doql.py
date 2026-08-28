import pytest

from mcp2doql.server import DoqlMCPServer, _require_mutation


def test_mcp_server_registers_tools() -> None:
    pytest.importorskip("mcp")
    server = DoqlMCPServer(name="test-doql")
    assert server.app is not None
    assert server.app.name == "test-doql"


def test_mcp_mutations_require_operator_capability(monkeypatch) -> None:
    monkeypatch.delenv("DOQL_MCP_ALLOW_MUTATION", raising=False)
    with pytest.raises(PermissionError, match="DOQL_MCP_ALLOW_MUTATION"):
        _require_mutation("doql_patch")

    monkeypatch.setenv("DOQL_MCP_ALLOW_MUTATION", "1")
    _require_mutation("doql_patch")
