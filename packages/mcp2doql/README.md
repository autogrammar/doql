# mcp2doql

**Serwer MCP** do sterowania manifestami DOQL (query, patch, validate, DSL).

Powiązane: [indeks paczek](../README.md) · [README główne doql](../../README.md) · [dsl2doql](../dsl2doql/README.md)

## Do czego służy

- uruchamia serwer **FastMCP (stdio)** z narzędziami DOQL
- deleguje logikę do `dsl2doql`, `uri2doql`, `nlp2doql`
- skanowanie MCP w projekcie → `doql adopt` (logika w `doql/adopt/scanner/interfaces/mcp.py`)

## CLI / MCP

```bash
pip install -e ../.. -e .
mcp2doql serve              # stdio MCP server
mcp2doql-mcp                # entry point MCP (pyproject.scripts)
```

Narzędzia MCP m.in.: `doql_query`, `doql_materialize`, `doql_validate`, `doql_run_dsl`, `doql_patch`, `doql_apply_nl`.

Operacje zapisujące lub wykonujące DSL są domyślnie zablokowane. Uruchom serwer
z `DOQL_MCP_ALLOW_MUTATION=1`, aby jawnie zezwolić zaufanym klientom MCP na
`materialize`, `patch`, `update`, `apply` i wykonanie DSL.

## Testy

```bash
pytest packages/mcp2doql/tests -q
```
