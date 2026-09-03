# Changelog

Wszystkie istotne zmiany w projekcie `doql`. Format oparty na [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

- Subject-bound, audited `digital-twin` declarations, CSS/YAML round-trip,
  validation and a domain-independent safe projection helper.
- Digital-twin projection now fails closed without explicit AQL evidence and
  an audit sink, recursively redacts nested secrets and bounds input graphs.
- The canonical parser and digital-twin runtime now pass strict mypy checks in
  CI; CSS workflow helpers are fully typed and interface page entity sources
  are represented explicitly instead of being attached dynamically.
- Strict CI coverage now includes YAML/CSS/Markdown import and export
  boundaries, including lossless page `entry` and `from_entity` metadata.
- All application, API, workflow, web, integration, i18n and infrastructure
  generators now pass strict mypy checks and are part of the CI type gate.
- The complete 154-file DOQL runtime now passes strict mypy, including CLI,
  plugins, adoption scanners and the optional OP3/redeploy/LSP boundaries.
- Fixed `workspace fix --dry-run` using `_tf_validate` without importing it.
- Restored LSP helper compatibility exports and added diagnostic publishing
  compatible with both pygls 1.x and 2.x.
- CI now installs the device-adoption extra, so OP3 adoption and drift tests
  execute instead of being silently skipped.

## [1.0.44] - 2026-09-03

### Docs
- Update README.md

### Other
- Update uv.lock
- Update vscode-doql/package-lock.json

## [1.0.43] - 2026-06-09

### Docs
- Update README.md
- Update packages/CONTROL_LAYER_PROMPT.template.md
- Update packages/README.md
- Update packages/rest2doql/README.md

### Other
- Update .gitignore
- Update app.doql.less
- Update doql/adopt/scanner/interfaces/cli.py
- Update doql/adopt/scanner/interfaces/mcp.py
- Update doql/cli/lockfile.py
- Update doql/importers/oql_converter.py
- Update packages/dsl2doql/proto/dsl2doql/v1/command.proto
- Update packages/dsl2doql/proto/dsl2doql/v1/result.proto
- Update packages/dsl2doql/scripts/generate-proto.sh
- Update packages/dsl2doql/src/dsl2doql/__init__.py
- ... and 29 more files

## [1.0.42] - 2026-06-08

### Docs
- Update README.md
- Update TODO.md
- Update packages/CONTROL_LAYER_PROMPT.template.md
- Update packages/README.md
- Update packages/cli2doql/README.md
- Update packages/dsl2doql/README.md
- Update packages/mcp2doql/README.md
- Update packages/nlp2doql/README.md
- Update packages/uri2doql/README.md

### Test
- Update tests/test_oql_converter.py
- Update tests/test_tooling_packages.py

### Other
- Update app.doql.less
- Update doql/adopt/scanner/interfaces/cli.py
- Update doql/adopt/scanner/interfaces/mcp.py
- Update doql/importers/__init__.py
- Update doql/importers/oql_converter.py
- Update packages/cli2doql/pyproject.toml
- Update packages/cli2doql/src/cli2doql/__init__.py
- Update packages/cli2doql/src/cli2doql/cli.py
- Update packages/cli2doql/src/cli2doql/scanner.py
- Update packages/cli2doql/tests/test_cli2doql.py
- ... and 23 more files

## [1.0.41] - 2026-06-08

### Docs
- Update README.md

### Other
- Update packages/dsl2doql/src/dsl2doql/cli.py
- Update packages/dsl2doql/tests/test_dsl2doql.py

## [1.0.40] - 2026-06-08

### Docs
- Update README.md
- Update packages/cli2doql/README.md
- Update packages/dsl2doql/README.md

### Test
- Update tests/test_parser_benchmark.py

### Other
- Update packages/cli2doql/pyproject.toml
- Update packages/cli2doql/src/cli2doql/__init__.py
- Update packages/cli2doql/src/cli2doql/cli.py
- Update packages/cli2doql/src/cli2doql/scanner.py
- Update packages/cli2doql/tests/test_cli2doql.py
- Update packages/dsl2doql/pyproject.toml
- Update packages/dsl2doql/src/dsl2doql/__init__.py
- Update packages/dsl2doql/src/dsl2doql/converter.py
- Update packages/mcp2doql/tests/test_mcp2doql.py

## [1.0.39] - 2026-06-08

### Docs
- Update README.md

### Other
- Update project/planfile-tickets.yaml

## [1.0.38] - 2026-06-08

### Docs
- Update README.md
- Update packages/mcp2doql/README.md

### Other
- Update packages/mcp2doql/pyproject.toml
- Update packages/mcp2doql/src/mcp2doql/__init__.py
- Update packages/mcp2doql/src/mcp2doql/cli.py
- Update packages/mcp2doql/src/mcp2doql/scanner.py

## [1.0.37] - 2026-06-08

### Docs
- Update README.md

### Test
- Update tests/test_parser_benchmark.py

### Other
- Update app.doql.less
- Update project/planfile-tickets.yaml

## [1.0.36] - 2026-06-08

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update packages/nlp2doql/README.md
- Update packages/uri2doql/README.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/integration/test_op3_bridge.py
- Update tests/test_adopt.py

### Other
- Update app.doql.less
- Update doql/adopt/scanner/__init__.py
- Update doql/adopt/scanner/deploy.py
- Update doql/adopt/scanner/environments.py
- Update doql/adopt/scanner/interfaces/__init__.py
- Update doql/adopt/scanner/interfaces/cli.py
- Update doql/adopt/scanner/interfaces/mcp.py
- Update doql/adopt/scanner/metadata.py
- Update doql/adopt/scanner/tests.py
- Update doql/adopt/scanner/workflows.py
- ... and 46 more files

## [1.0.35] - 2026-04-25

### Docs
- Update README.md

## [1.0.34] - 2026-04-25

### Docs
- Update README.md

## [1.0.33] - 2026-04-25

### Docs
- Update README.md

## [1.0.32] - 2026-04-25

### Docs
- Update README.md

### Test
- Update tests/test_deploy.py

## [1.0.31] - 2026-04-25

### Docs
- Update README.md

## [1.0.30] - 2026-04-25

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update TODO.md
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Other
- Update VERSION
- Update app.doql.less
- Update doql/__init__.py
- Update doql/adopt/scanner/interfaces.py
- Update doql/adopt/scanner/interfaces/__init__.py
- Update doql/adopt/scanner/interfaces/api.py
- Update doql/adopt/scanner/interfaces/cli.py
- Update doql/adopt/scanner/interfaces/desktop.py
- Update doql/adopt/scanner/interfaces/mobile.py
- Update doql/adopt/scanner/interfaces/web.py
- ... and 76 more files

## [1.0.28] - 2026-04-24

### Docs
- Update README.md

### Other
- Update doql/adopt/scanner/metadata.py
- Update doql/cli/commands/adopt.py

## [1.0.27] - 2026-04-24

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update docs/README.md
- Update examples/SUMD.md
- Update project/README.md
- Update project/context.md
- Update vscode-doql/SUMD.md

### Test
- Update tests/env_manager.py
- Update tests/test_adopt.py
- Update tests/test_runtime.py

### Other
- Update app.doql.less
- Update doql/exporters/css/renderers.py
- Update examples/project/map.toon.yaml
- Update project/analysis.toon.yaml
- Update project/calls.mmd
- Update project/calls.png
- Update project/calls.toon.yaml
- Update project/calls.yaml
- Update project/compact_flow.mmd
- Update project/compact_flow.png
- ... and 12 more files

## [1.0.26] - 2026-04-23

### Docs
- Update README.md

## [1.0.25] - 2026-04-23

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Other
- Update app.doql.css
- Update app.doql.less
- Update project/analysis.toon.yaml
- Update project/calls.mmd
- Update project/calls.png
- Update project/calls.toon.yaml
- Update project/calls.yaml
- Update project/compact_flow.mmd
- Update project/compact_flow.png
- Update project/duplication.toon.yaml
- ... and 8 more files

## [1.0.24] - 2026-04-23

### Other
- Update project.sh

## [1.0.23] - 2026-04-23

### Other
- Update app.doql.less
- Update project.sh

## [1.0.22] - 2026-04-23

### Docs
- Update README.md

### Test
- Update tests/test_adopt.py
- Update tests/test_css_parser.py
- Update tests/test_exporters.py

## [1.0.21] - 2026-04-23

### Docs
- Update README.md

### Other
- Update doql/cli/commands/adopt.py

## [1.0.20] - 2026-04-23

### Docs
- Update README.md

### Other
- Update doql/cli/main.py
- Update doql/exporters/css/__init__.py
- Update doql/exporters/css/renderers.py
- Update doql/parsers/__init__.py
- Update doql/parsers/blocks.py
- Update doql/parsers/css_mappers.py
- Update doql/parsers/css_parser.py
- Update doql/parsers/css_utils.py
- Update doql/parsers/models.py
- Update doql/parsers/registry.py

## [1.0.19] - 2026-04-23

### Test
- Update tests/test_parser_benchmark.py

### Other
- Update doql/parsers/models.py

## [1.0.18] - 2026-04-23

### Other
- Update doql/parsers/css_parser.py
- Update doql/parsers/css_tokenizer.py

## [1.0.17] - 2026-04-23

### Other
- Update doql/exporters/css/__init__.py

## [1.0.16] - 2026-04-23

### Docs
- Update README.md

## [1.0.15] - 2026-04-23

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update docs/README.md
- Update examples/SUMD.md
- Update examples/SUMR.md
- Update plugins/doql-plugin-erp/SUMD.md
- Update plugins/doql-plugin-fleet/SUMD.md
- Update plugins/doql-plugin-gxp/SUMD.md
- Update plugins/doql-plugin-iso17025/SUMD.md
- ... and 5 more files

### Other
- Update app.doql.css
- Update app.doql.less
- Update doql/adopt/scanner/deploy.py
- Update doql/adopt/scanner/environments.py
- Update doql/adopt/scanner/interfaces.py
- Update doql/adopt/scanner/metadata.py
- Update doql/exporters/css/__init__.py
- Update doql/exporters/css/renderers.py
- Update doql/parsers/models.py
- Update examples/app.doql.less
- ... and 28 more files

## [1.0.14] - 2026-04-21

### Docs
- Update PARSER_AUDIT.md
- Update README.md

### Test
- Update tests/integration/test_adopt_from_device.py

## [1.0.13] - 2026-04-21

### Docs
- Update README.md
- Update SPEC.md
- Update SUMD.md
- Update SUMR.md
- Update docs/README.md
- Update project/README.md
- Update project/context.md

### Other
- Update app.doql.less
- Update plugins/doql-plugin-erp/.github/workflows/doql-ci.yml
- Update plugins/doql-plugin-erp/sumd.json
- Update plugins/doql-plugin-fleet/.github/workflows/doql-ci.yml
- Update plugins/doql-plugin-fleet/sumd.json
- Update plugins/doql-plugin-gxp/.github/workflows/doql-ci.yml
- Update plugins/doql-plugin-gxp/sumd.json
- Update plugins/doql-plugin-iso17025/.github/workflows/doql-ci.yml
- Update plugins/doql-plugin-iso17025/sumd.json
- Update plugins/doql-plugin-shared/.github/workflows/doql-ci.yml
- ... and 18 more files

## [1.0.12] - 2026-04-21

### Docs
- Update README.md

### Other
- Update app.doql.less

## [1.0.11] - 2026-04-21

### Docs
- Update README.md
- Update SUMD.md
- Update plugins/doql-plugin-shared/SUMD.md

### Other
- Update Jenkinsfile
- Update app.doql.css
- Update app.doql.less
- Update doql/generators/infra_gen.py
- Update doql/parsers/css_mappers.py
- Update plugins/doql-plugin-shared/project/map.toon.yaml
- Update plugins/doql-plugin-shared/sumd.json
- Update project/map.toon.yaml
- Update sumd.json

## [1.0.10] - 2026-04-21

### Docs
- Update README.md
- Update analysis-20260421/doql_playground/context.md
- Update code2llm_output/doql_playground/context.md
- Update code2llm_output/plugins/context.md
- Update docs/doql_playground/analysis.toon.yaml
- Update docs/doql_playground/context.md
- Update docs/doql_playground/evolution.toon.yaml
- Update docs/plugins/context.md
- Update examples/blog-cms/docs/index.md

### Other
- Update .redeploy/state/infra-local-9dd2f59b.yaml
- Update analysis-20260421/doql_playground/analysis.toon.yaml
- Update analysis-20260421/doql_playground/evolution.toon.yaml
- Update analysis/doql_playground/analysis.toon.yaml
- Update app.doql.less
- Update code2llm_output/doql_playground/analysis.toon.yaml
- Update code2llm_output/doql_playground/evolution.toon.yaml
- Update code2llm_output/doql_playground/flow.toon.yaml
- Update code2llm_output/plugins/evolution.toon.yaml
- Update code2llm_output/plugins/flow.toon.yaml
- ... and 36 more files

## [1.0.9] - 2026-04-21

### Docs
- Update README.md

### Other
- Update doql/integrations/op3_bridge.py

## [1.0.8] - 2026-04-21

### Docs
- Update README.md
- Update SUMD.md
- Update docs/README.md
- Update plugins/doql-plugin-erp/SUMD.md
- Update plugins/doql-plugin-erp/SUMR.md
- Update plugins/doql-plugin-fleet/SUMD.md
- Update plugins/doql-plugin-fleet/SUMR.md
- Update plugins/doql-plugin-gxp/SUMD.md
- Update plugins/doql-plugin-gxp/SUMR.md
- Update plugins/doql-plugin-iso17025/SUMD.md
- ... and 5 more files

### Other
- Update plugins/doql-plugin-erp/app.doql.less
- Update plugins/doql-plugin-erp/project/map.toon.yaml
- Update plugins/doql-plugin-erp/sumd.json
- Update plugins/doql-plugin-fleet/app.doql.less
- Update plugins/doql-plugin-fleet/project/map.toon.yaml
- Update plugins/doql-plugin-fleet/sumd.json
- Update plugins/doql-plugin-gxp/app.doql.less
- Update plugins/doql-plugin-gxp/project/map.toon.yaml
- Update plugins/doql-plugin-gxp/sumd.json
- Update plugins/doql-plugin-iso17025/app.doql.less
- ... and 24 more files

## [1.0.7] - 2026-04-21

### Docs
- Update README.md

### Test
- Update tests/integration/test_build_from_device.py
- Update tests/integration/test_op3_bridge.py

### Other
- Update doql/cli/build.py
- Update doql/cli/main.py
- Update doql/integrations/op3_bridge.py

## [1.0.6] - 2026-04-21

### Docs
- Update README.md
- Update TODO.md
- Update docs/README.md

### Test
- Update tests/integration/__init__.py
- Update tests/integration/test_adopt_from_device.py
- Update tests/integration/test_drift.py
- Update tests/integration/test_op3_bridge.py

### Other
- Update Taskfile.yml
- Update doql/adopt/device_scanner.py
- Update doql/cli/commands/__init__.py
- Update doql/cli/commands/adopt.py
- Update doql/cli/commands/drift.py
- Update doql/cli/main.py
- Update doql/drift/__init__.py
- Update doql/drift/detector.py
- Update doql/integrations/__init__.py
- Update doql/integrations/op3_bridge.py
- ... and 2 more files

## [1.0.5] - 2026-04-21

### Docs
- Update README.md
- Update TODO.md
- Update docs/README.md

### Test
- Update tests/test_adopt.py
- Update tests/test_exporters_shims.py

### Other
- Update project.sh
- Update project/duplication.toon.yaml
- Update project/validation.toon.yaml

## [1.0.4] - 2026-04-20

### Docs
- Update CHANGELOG.md
- Update TODO.md

### Other
- Update .coverage
- Update .coveragerc
- Update doql/adopt/scanner/entities.py
- Update doql/cli/commands/doctor.py
- Update doql/cli/main.py

## [1.0.3] - 2026-04-20

### Added
- `doql doctor --fix` — auto-remediation for missing .env, migration.yaml hints, deprecated strategy warnings
- `pytest-cov` integration with `.coveragerc` (target 45% coverage)
- CSS tokenizer fix: proper handling of multiple declarations per line

### Changed
- Improved `_parse_declarations()` to split by semicolons before parsing
- Updated P0 blockers status in TODO.md

## [1.0.2] - 2026-04-20

### Docs
- Update README.md
- Update docs/refactoring-plan.md

### Other
- Update doql/cli/commands/doctor.py

## [1.0.1] - 2026-04-20

### Docs
- Update CHANGELOG.md
- Update README.md
- Update docs/refactoring-plan.md

### Test
- Update tests/test_css_parser.py
- Update tests/test_parser.py
- Update tests/test_parser_benchmark.py

### Other
- Update VERSION
- Update doql/__init__.py
- Update doql/cli/commands/doctor.py
- Update doql/parsers/css_parser.py
- Update doql/parsers/css_tokenizer.py
- Update doql/parsers/validators.py
- Update examples/todo-pwa/app.doql
- Update examples/todo-pwa/app.doql.css
- Update plugins/doql-plugin-erp/sumd.json
- Update plugins/doql-plugin-fleet/sumd.json
- ... and 3 more files

## [1.0.0] - 2026-04-20

### Added
- **Stable Public API** (`doql/__init__.py`) z jawny `__all__` — kontrakt semver zaczyna obowiązywać
- **CSS-like syntax support** (`.doql.css`, `.doql.less`, `.doql.sass`) jako alternatywa dla klasycznego `.doql`
- **Regression tests** porównujące `.doql` vs `.doql.less` dla tych samych projektów

### Changed (Breaking)
- **Nazewnictwo strategii deploymentu** zunifikowane z `redeploy`:
  - `docker-compose` → `docker_full` (stare działa jako alias)
  - `quadlet` → `podman_quadlet` (stare działa jako alias)
  - `kubernetes` → `k3s`
- **Optional dependency** `doql[deploy]` wymaga `redeploy>=0.2.0`

### Deprecated
- Klasyczny format `.doql` — parser działa, ale nowe projekty powinny używać `.doql.css` lub `.doql.less`

### Migration Guide
```bash
# 1. Zaktualizuj dependency
pip install "doql[deploy]>=1.0.0"

# 2. Sprawdź czy projekt się parsuje
doql validate

# 3. Zbuduj i przetestuj
doql build && doql run
```

## [0.1.12] - 2026-04-20

### Docs
- Update docs/README.md
- Update plugins/doql-plugin-erp/SUMD.md
- Update plugins/doql-plugin-fleet/SUMD.md
- Update plugins/doql-plugin-gxp/SUMD.md
- Update plugins/doql-plugin-iso17025/SUMD.md
- Update plugins/doql-plugin-shared/SUMD.md
- Update project/README.md
- Update project/context.md

### Other
- Update doql/adopt/scanner/entities.py
- Update doql/parsers/css_mappers.py
- Update plugins/doql-plugin-erp/project/map.toon.yaml
- Update plugins/doql-plugin-erp/sumd.json
- Update plugins/doql-plugin-fleet/project/map.toon.yaml
- Update plugins/doql-plugin-fleet/sumd.json
- Update plugins/doql-plugin-gxp/project/map.toon.yaml
- Update plugins/doql-plugin-gxp/sumd.json
- Update plugins/doql-plugin-iso17025/project/map.toon.yaml
- Update plugins/doql-plugin-iso17025/sumd.json
- ... and 19 more files

## [0.1.11] - 2026-04-20

### Docs
- Update README.md

### Other
- Update doql/cli/commands/deploy.py
- Update doql/cli/commands/quadlet.py
- Update doql/generators/infra_gen.py

## [0.1.10] - 2026-04-19

### Other
- Update doql/cli/commands/doctor.py
- Update doql/lsp_server.py

## [0.1.9] - 2026-04-19

### Other
- Update doql/adopt/scanner/entities.py
- Update doql/adopt/scanner/interfaces.py
- Update doql/adopt/scanner/roles.py
- Update doql/adopt/scanner/workflows.py
- Update doql/cli/sync.py
- Update doql/generators/workflow_gen.py
- Update doql/parsers/css_tokenizer.py
- Update doql/parsers/css_transformers.py

## [0.1.8] - 2026-04-19

### Other
- Update doql/cli/commands/doctor.py
- Update doql/cli/commands/run.py
- Update doql/cli/commands/validate.py
- Update doql/cli/lockfile.py
- Update doql/generators/api_gen/alembic.py

## [0.1.7] - 2026-04-19

### Other
- Update doql/adopt/scanner/databases.py
- Update doql/adopt/scanner/integrations.py
- Update doql/cli/commands/doctor.py
- Update doql/cli/commands/export.py
- Update doql/cli/commands/workspace.py
- Update doql/exporters/css/format_convert.py
- Update doql/generators/web_gen/pages.py
- Update doql/lsp_server.py
- Update doql/parsers/css_tokenizer.py

## [0.1.6] - 2026-04-19

### Other
- Update doql/parsers/css_transformers.py

## [0.1.5] - 2026-04-19

### Docs
- Update README.md

### Other
- Update doql/adopt/scanner/entities.py
- Update doql/adopt/scanner/workflows.py
- Update doql/parsers/css_mappers.py
- Update doql/parsers/css_tokenizer.py

## [0.1.4] - 2026-04-19

### Docs
- Update CHANGELOG.md
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update TODO.md

### Test
- Update testql-scenarios/generated-api-smoke.testql.toon.yaml

### Other
- Update Taskfile.yml
- Update doql/cli/main.py
- Update project/map.toon.yaml
- Update sumd.json

## [0.1.3] - 2026-04-19

### Added
- testql-scenarios: `generated-api-smoke.testql.toon.yaml` — API smoke tests
- testql-scenarios: `generated-api-integration.testql.toon.yaml` — API integration flows
- testql-scenarios: `generated-from-pytests.testql.toon.yaml` — scenarios from pytest suite

### Docs
- Removed AI cost tracking badges from README
- Version badge updated to 0.1.3

### Added (sesja 13 — doql adopt + environments)
- **`doql adopt`** command — reverse-engineer existing project into `app.doql.css`.
  Scans `pyproject.toml`, `package.json`, `.env`, `Dockerfile`, `docker-compose.yml`,
  SQL `CREATE TABLE`, Python model classes. Detects API (FastAPI/Flask/Django),
  CLI (click/argparse), Web (React/Vue/Svelte), Mobile, Desktop interfaces.
  Implementation: `doql/adopt/scanner.py` (~400 lines) + `doql/adopt/emitter.py`.
- **`Environment` model** — `environment[name="prod"] { runtime: quadlet; ssh_host: ...; }`
  New dataclass in `parsers/models.py`, CSS mapper `_map_environment`, CSS renderer
  `_render_environment`, full round-trip support across all formats.
- Generated manifests for 5 oqlos sibling projects: oql, oqlos, testql, weboql, www.

### Fixed (sesja 13)
- **Interface lookup** — changed from `i.type == itype` to `i.name == itype` in
  `_map_interface`, preventing duplicates when `type` declaration differs from selector.
- **Interface renderer** — now uses `interface[type="..."]` instead of `interface[name="..."]`.
- **Duplicate pages** — added deduplication in web frontend scanner.
- **SQL entity parser** — filtered REFERENCES/CASCADE/etc. from field names.

### Added (sesja 14 — doctor, publish, deploy directives)
- **`doql doctor`** — comprehensive 9-check health diagnostic: parse validation,
  env vars coverage, file references, database config, interface consistency,
  required tools on PATH, deploy config, environment definitions. Optional
  `--env <name>` runs remote SSH diagnostics (connectivity, runtime, disk space).
- **`doql build --no-overwrite`** — merge-friendly build that generates into temp
  directory and copies only new files to `build/`, skipping existing ones.
- **Deploy directives `@local`/`@push`/`@remote`** — CSS tokenizer updated to accept
  `@`-prefixed property names. New `Deploy.directives: dict[str, str]` field. Parsed
  in `_map_deploy`, rendered in `_render_deploy`. `doql deploy` executes them in
  order: local → push → remote, falling back to docker-compose if no directives.
- **`doql publish`** — publish artifacts to PyPI (twine), npm, Docker/Podman registries,
  GitHub Releases (gh CLI). Flags: `--target pypi,npm,docker,github`, `--dry-run`.
- **Test suite: 130 passed**, 3 skipped (pygls, 2× psycopg2).
- **CLI: 19 subcommands** (added: adopt, doctor, publish).

### Fixed (sesja 14)
- **Workflow generator** — `_step_fn_name()` sanitizes special characters (`+`, etc.)
  from step action names, preventing invalid Python function names like
  `step_hash_+_sign_certificate_pdf`.

#### Project metrics (sesja 14)
| Metric | Value |
|--------|-------|
| Source files | 92 |
| Lines of code | ~10,500 |
| Tests | 130 passed, 3 skipped |
| CLI subcommands | 19 |
| Examples | 10 |
| Plugins | 4 |
| Scaffold templates | 4 |

### W toku
- Parser tree-sitter (pełna gramatyka `.doql`, error recovery)
- Rozszerzenie VS Code o `.doql.css` / `.doql.less` / `.doql.sass`
- Pilot w realnej firmie

### Refactored (sesja 11 — static-analysis-driven refactoring)
- **css_exporter split** — 423-line monolith `css_exporter.py` → package
  `doql/exporters/css/` (`helpers.py`, `renderers.py`, `format_convert.py`,
  `__init__.py`). Old module kept as backward-compat re-export shim.
- **markdown_exporter split** — 225-line `markdown_exporter.py` → package
  `doql/exporters/markdown/` (`sections.py`, `writers.py`, `__init__.py`).
  Old module kept as backward-compat shim.
- **css_parser extract** — `_tokenise_css` and `_parse_declarations`
  extracted to `doql/parsers/css_tokenizer.py` (was inline in 213-line
  `css_parser.py`).
- **Shared `_clean`** — recursive dict cleaner extracted from
  `yaml_exporter.py` to `doql/utils/clean.py`.
- **`_createBuildFunction` split** — 110-line Python string template
  extracted from `playground/pyodide-bridge.js` to standalone
  `playground/doql_build.py` with 6 named helpers (`_collect_parse_errors`,
  `_build_env`, `_validate`, `_spec_summary`, `_try_generate`, `build`).
  JS now fetches the `.py` file at boot time.
- **yaml_importer docstrings** — added docstrings to all 17 builder
  functions in `doql/importers/yaml_importer.py`.

### Fixed (sesja 11)
- **`gen_auth` indentation bug** — multi-line `user_model_def` interpolated
  inside `textwrap.dedent(f'...')` broke line alignment; `auth.py` started
  with unexpected indent for specs without a `User` entity
  (e.g. calibration-lab). Fixed via `textwrap.indent` pre-alignment.

### Added (sesja 12 — full runtime testing)
- **`tests/test_runtime.py`** — 18 new pytest tests: 8 API boot+health
  tests (uvicorn launched per example, /health + /openapi.json verified)
  and 10 build-target artifact checks (web/mobile/desktop/infra per example).
- **`test_generators.py`** expanded from 5 → 10 examples (added blog-cms,
  crm-contacts, e-commerce-shop, notes-app, todo-pwa).
- **`runtime_all_examples.sh`** updated: all 10 examples, auto-skip
  postgres-dependent APIs, `auth.py` compile check, `python-multipart`
  auto-install in runtime venv.
- **Test suite: 120 tests** (99 → 120), 4 skipped
  (2 sqlalchemy plugin, 2 psycopg2/postgres).

### Fixed (sesja 12)
- **Runtime `python-multipart`** — generated `auth.py` uses
  `OAuth2PasswordRequestForm` (form data) which requires
  `python-multipart`; added to runtime venv deps.

#### Metrics (before → after)
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| CC avg | 3.20 | 3.11 | < 2.5 |
| God modules (>300L) | 7 | 5 | 0 |
| Fan-out ≥ 8 | 20 | 9 | < 10 |
| Import cycles | 2 | 0 | 0 |

### Added (sesja 10 — CSS-like format + export/import + examples)
- **CSS-like parser** — full parser for `.doql.css`, `.doql.less`, `.doql.sass`
  formats (9 modules: `css_parser`, `css_utils`, `css_mappers`,
  `css_transformers`). All formats produce identical `DoqlSpec`.
- **LESS variables** (`@var`) and **SASS variables** (`$var`) are resolved
  during parsing; result is variable-free `DoqlSpec`.
- **Auto-detection** — `detect_doql_file()` priority:
  `.doql.less` > `.doql.sass` > `.doql.css` > `.doql`
- **Exporters** — `doql/exporters/`: `yaml_exporter.py`, `markdown_exporter.py`,
  `css_exporter.py` (supports CSS, LESS, SASS output).
- **Importer** — `doql/importers/yaml_importer.py`: YAML → `DoqlSpec`.
- **CLI `import` command** — `doql import spec.yaml -o app.doql`.
- **CLI `export` formats** expanded: `yaml`, `markdown`, `css`, `less`, `sass`
  (in addition to existing `openapi`, `postman`, `typescript-sdk`).
- **5 new examples**: `blog-cms` (SASS), `crm-contacts` (LESS),
  `e-commerce-shop` (CSS), `notes-app` (SASS), `todo-pwa` (CSS).
  Each example has both classic `.doql` and CSS-like format.
- **Test suite expanded** to **99 tests** (from 38): 13 CSS parser tests,
  28 exporter tests, plus parametrized example validation.

### Fixed (sesja 10)
- **Validator**: absolute DATA file paths (e.g. `/var/lib/kiosk/...`) now
  produce warnings instead of errors — they are deployment targets.
- **Validator**: env wildcard patterns (`env.SMTP_*`) no longer produce
  false-positive warnings. Prefix matching implemented for trailing `_` refs.
- **validate command**: now uses `detect_doql_file()` instead of hardcoded
  `"app.doql"` — correctly finds CSS-like format files.
- **asset-management example**: added missing `User` entity (referenced by
  `Station.manager`).
- **calibration-lab example**: added missing `Operator` entity (referenced by
  `Calibration.performed_by` / `reviewed_by`).
- **SPEC.md updated** to v0.2.1 — added sections 16 (CSS-like syntax),
  17 (Export/Import).

### Added (sesja 8 — full-stack examples + env manager)
- **Mobile PWA generator** (`doql/generators/mobile_gen.py`) — replaces the
  earlier stub. Now emits a self-contained installable PWA: `manifest.json`,
  `service-worker.js` (cache-first shell, network-first API), entity-aware
  CRUD `app.js`, mobile-first `style.css`, and SVG icons.
- **Tauri v2 desktop generator** — `desktop_gen.py` upgraded from Tauri 1.5
  (which required deprecated `webkit2gtk-4.0` + `libsoup-2.4`) to Tauri 2.x
  (uses `webkit2gtk-4.1` + `libsoup-3.0` available on Ubuntu 24.04+).
  Generates a placeholder RGBA `icons/icon.png` so `tauri dev` compiles
  out-of-the-box; bundling disabled by default.
- **New examples**:
  - `examples/notes-app/` — full-stack demo (API + web + mobile + desktop)
  - `examples/todo-pwa/` — minimal mobile-first PWA demo
- **Environment manager** (`tests/env_manager.py`) — discovers every
  `examples/*/app.doql`, runs `doql build`, and verifies all 5 generated
  layers per example: API (compile + uvicorn boot + `/health` + OpenAPI),
  web (package.json/vite/tsconfig/.tsx), mobile (manifest+SW+icons),
  desktop (tauri.conf.json v1/v2, Cargo.toml, optional `cargo check`),
  infra (compose+Dockerfile). Outputs both human-readable table and
  `--json`. CLI flags: `--skip-api`, `--cargo-check`, `--verbose`.
- **Playground**: `.env` tab showing seeded localhost defaults + spec
  references; URL hash sync (`#tab=ast` deep-links).

### Added (Faza 3 — Ecosystem, sesja 6)
- **`doql-plugin-iso17025`** — ISO/IEC 17025:2017: traceability chain, GUM
  uncertainty budgets (u_c = √Σ(cᵢ·uᵢ)²), calibration certificates, drift
  monitor (linear regression vs CMC).
- **`doql-plugin-fleet`** — multi-tenant fleet manager: `Tenant` model +
  `TenantMiddleware` (X-Tenant-Id / subdomain / JWT), device registry
  (`/enroll`, `/heartbeat`, `/health`), `MetricSample` time-series,
  OTA canary rollout with state machine.
- **`doql-plugin-erp`** — Odoo XML-RPC client, mapping DSL, bidirectional
  sync with conflict policies, inbound webhook handlers (HMAC-verified).
- **Marketplace scaffolds** — `saas-multi-tenant`, `calibration-lab`,
  `iot-fleet`; new CLI flag `doql init --list-templates`.

### Added (Faza 2 — sesja 7)
- **Test suite** — 99 pytest tests covering parser, CSS parser, exporters,
  generators, plugins, LSP + GUM numerics; `tests/runtime_deploy.sh` end-to-end runtime smoke;
  `tests/runtime_all_examples.sh` multi-example /health probe;
  `tests/playground_e2e.py` headless Playwright verification.
- **Packaging** — `pyproject.toml` `package-data` ships `scaffolds/**/*`
  with the wheel; 5 wheels build cleanly (doql + 4 plugins). Fresh-venv
  install verified.
- **CI** — `.github/workflows/ci.yml` with matrix unit-tests (3.10–3.13),
  runtime-smoke job (API + all examples + web build), packaging job
  (sdist + wheel + fresh-venv verification + artifact upload), and a
  playground deploy job (GitHub Pages, main-only).
- **Playground** — `playground/` static HTML+Pyodide app runs the real
  `doql` wheel client-side. Live editor → parser + validator + generator
  diagnostics + generated `models.py` / `schemas.py` preview. No backend,
  no telemetry, ~65 kB wheel served once per session. Deploys to
  GitHub Pages / Netlify / S3.

### Fixed (runtime bugs found during deploy verification, sesja 7)
- API generator: auto-inject `id` primary key when an entity has no `id`
  field (was: `sqlalchemy.exc.ArgumentError: could not assemble any
  primary key columns`).
- API generator: `_py_type` wraps all non-required / auto fields in
  `Optional[…]` (was: `ResponseValidationError: Input should be a valid
  string` for nullable columns under Pydantic v2 strict mode).
- API generator: CRUD routes auto-generate UUID `id` on POST.
- API generator: `id: Optional[str]` injected into response schema for
  auto-PK entities so clients see the generated id.
- API generator: drop FK constraint when the referenced entity is not in
  the spec (was: `NoReferencedTableError` at app startup).
- API generator: pin `bcrypt>=4.0,<4.1` in `requirements.txt` (passlib
  1.7.x is broken on bcrypt 4.1+ due to removed `__about__` attribute).
- Parser `ROLES`: match `^  name:` not `- word` (was: nested permission
  verbs like `read`, `execute` were extracted as role names).
- Auth generator: use `role.name` instead of stringifying the whole
  `Role` dataclass into the `ROLES = [...]` allowlist.
- Web generator: prepend `id: any` to the TS entity interface when the
  entity has no explicit id field (TSX was `TS2339: Property 'id' does
  not exist`).


## [0.1.3] - 2026-04-19

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update plugins/doql-plugin-erp/SUMD.md
- Update plugins/doql-plugin-erp/SUMR.md
- Update plugins/doql-plugin-fleet/SUMD.md
- Update plugins/doql-plugin-fleet/SUMR.md
- Update plugins/doql-plugin-gxp/SUMD.md
- Update plugins/doql-plugin-gxp/SUMR.md
- Update plugins/doql-plugin-iso17025/SUMD.md
- ... and 3 more files

### Test
- Update tests/test_adopt.py

### Other
- Update doql/adopt/emitter.py
- Update doql/cli/commands/adopt.py
- Update doql/cli/main.py
- Update project/map.toon.yaml
- Update sumd.json

## [0.1.2] - 2026-04-18

### Docs
- Update README.md

## [0.1.1] - 2026-04-18

### Other
- Update Taskfile.yml
- Update VERSION
- Update doql/__init__.py
- Update doql/parsers/css_transformers.py
- Update pyqual.yaml

## [0.0.3] - 2026-04-18

### Docs
- Update README.md

### Other
- Update doql/adopt/scanner/__init__.py
- Update doql/adopt/scanner/environments.py
- Update doql/generators/workflow_gen.py
- Update doql/parsers/css_mappers.py
- Update doql/parsers/css_transformers.py

## [0.0.2] - 2026-04-17

### Docs
- Update GLOSSARY.md
- Update README.md
- Update articles/01-oqlos-status-2026-q2.md
- Update articles/02-testql-status-2026-q2.md
- Update articles/05-wizja-ekosystemu-oqlos.md
- Update articles/06-doql-v02-dokumenty-kiosk.md

### Other
- Update doql/__init__.py
- Update examples/asset-management/app.doql.css

## [0.0.1] - 2026-04-17

### Docs
- Update README.md
- Update TODO/01-doql-format-migration-analysis.md
- Update TODO/02-doql-css-iot-fleet-example.md
- Update TODO/03-doql-less-calibration-lab-example.md
- Update TODO/04-doql-sass-notes-app-example.md
- Update TODO/05-doql-migration-guide.md
- Update TODO/README.md
- Update docs/README.md
- Update examples/notes-app/build/desktop/README.md
- Update project/README.md
- ... and 1 more files

### Test
- Update test_all_desktop.yml
- Update test_desktop_builds.yml
- Update test_playbook.yml

### Other
- Update .gitignore
- Update doql.sh
- Update doql/cli.py
- Update doql/cli/__init__.py
- Update doql/cli/build.py
- Update doql/cli/commands/__init__.py
- Update doql/cli/commands/deploy.py
- Update doql/cli/commands/docs.py
- Update doql/cli/commands/export.py
- Update doql/cli/commands/generate.py
- ... and 57 more files

## [0.2.0-alpha] — 2026-04-16

Rozszerzenie zakresu: dokumenty, dane, kiosk, jednoznaczna semantyka.

### Added

#### Język i specyfikacja
- Nowy dokument `GLOSSARY.md` — jednoznaczna semantyka OQL / DOQL / IQL
- SPEC v0.2 — 16 sekcji (z 11 w v0.1)
- Nowy typ sekcji `DATA` — źródła danych: JSON, SQLite, API, CSV, Excel, ENV
- Nowy typ sekcji `TEMPLATE` — reużywalne szablony
- Nowy typ sekcji `DOCUMENT` — generowanie PDF/HTML/DOCX/Markdown
- Nowy typ sekcji `REPORT` — okresowe raporty z agregacją
- Nowy typ sekcji `DATABASE` — jawne deklarowanie bazy
- Nowy typ sekcji `API_CLIENT` — klienty do zewnętrznych API
- Nowy typ sekcji `WEBHOOK` — handlery zdarzeń przychodzących
- Nowy typ interfejsu `INTERFACE kiosk` — stanowiska pełnoekranowe
- Nowy target deploy `kiosk-appliance` — Raspberry Pi / tablet

#### Przykłady
- `examples/document-generator/` — generator świadectw ISO 17025 (bez ciężkiego SaaS)
- `examples/kiosk-station/` — stanowisko operatora na tablecie

#### Dokumentacja
- Zaktualizowany `README.md` z rozszerzonym zakresem
- Zaktualizowany `OQLOS-REQUIREMENTS.md` — 3 nowe wymagania (webhook push, execution data, delta API)

### Changed
- `INTERFACE web/mobile/desktop` mogą teraz korzystać z `DATA` sources bezpośrednio
- `DEPLOY` wspiera 3 targety: `docker-compose`, `quadlet`, `kiosk-appliance`
- Quadlet generator produkuje też Traefik jako Quadlet (a nie zwykły docker-compose)

### Known Limitations
- Parser v0.2 jeszcze w trakcie implementacji
- Generator PDF przez WeasyPrint — pełne CSS3 grid jeszcze nie działa
- Kiosk appliance tylko dla Raspberry Pi OS (Windows IoT / Ubuntu Kiosk w v0.3)

## [0.1.0-alpha] — 2026-04-16

Pierwsza publiczna wersja — specyfikacja języka i przykłady SaaS.

### Added
- Specyfikacja języka `doql` v0.1 (SPEC.md)
- Trzy kompletne przykłady deklaracji:
  - `examples/asset-management/` — klon Drägerware
  - `examples/calibration-lab/` — lab ISO 17025
  - `examples/iot-fleet/` — flota urządzeń IoT
- Szkielet CLI (`doql init`, `validate`, `plan`, `build`, `run`, `deploy`, `sync`, `export`, `docs`)
- Dokument `OQLOS-REQUIREMENTS.md` z listą zmian wymaganych w oqlos
- Dokument `ROADMAP.md` z planem faz 0–3

---

## Przyszłe wersje

### [0.3.0] — planowane Lipiec 2026
- LSP dla VS Code + składnia
- Playground online (playground.doql.dev)
- Kubernetes target (Helm chart)
- Flutter mobile generator
- Windows IoT / Ubuntu Kiosk targets

### [0.5.0] — planowane Wrzesień 2026
- Pierwszy pilot w produkcji
- Marketplace szablonów `.doql`
- `doql sync` (merge-friendly)
- Import z Postmana / OpenAPI do `.doql`

### [1.0.0] — planowane Q4 2026
- Stabilne API, backwards compatibility guarantee
- Pełen zestaw szablonów domenowych
- Certyfikacja deweloperów
- Commercial plugins (gxp, iso17025, fleet)
