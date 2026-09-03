"""doql — Declarative OQL.

Build complete applications, documents, kiosks, and API integrations
from a single .doql declaration file.

Public API (stable since v1.0.0):
    parse_file(path) -> DoqlSpec
    parse_text(text) -> DoqlSpec
    validate(spec, env_vars) -> list[ValidationIssue]
    build(ctx) -> BuildContext
    deploy(ctx, dry_run) -> int

Example:
    import doql
    spec = doql.parse_file(pathlib.Path("app.doql"))
    issues = doql.validate(spec, env_vars={"DOMAIN": "example.com"})
"""

__version__ = "1.0.44"

# Re-export stable public API from parsers
from doql.parsers import (
    parse_file,
    parse_text,
    parse_env,
    validate,
    DoqlSpec,
    DoqlParseError,
    ValidationIssue,
    Entity,
    EntityField,
    DataSource,
    Template,
    Document,
    Report,
    Database,
    ApiClient,
    Webhook,
    Page,
    Interface,
    Integration,
    Workflow,
    WorkflowStep,
    Role,
    Deploy,
    detect_doql_file,
)

# Re-export CSS-like parser (stable since v1.0.0)
from doql.parsers import (
    parse_css_file,
    parse_css_text,
    CssBlock,
    ParsedSelector,
)

__all__ = [
    # Version
    "__version__",
    # Main entry points
    "parse_file",
    "parse_text",
    "parse_env",
    "validate",
    "detect_doql_file",
    # Models (core data structures)
    "DoqlSpec",
    "DoqlParseError",
    "ValidationIssue",
    "Entity",
    "EntityField",
    "DataSource",
    "Template",
    "Document",
    "Report",
    "Database",
    "ApiClient",
    "Webhook",
    "Page",
    "Interface",
    "Integration",
    "Workflow",
    "WorkflowStep",
    "Role",
    "Deploy",
    # CSS-like parser (pluggable syntax)
    "parse_css_file",
    "parse_css_text",
    "CssBlock",
    "ParsedSelector",
]
