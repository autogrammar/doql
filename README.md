# Rodzina OQL — paczka kompletna

## Digital twin — własny obraz aktora

DOQL może deklarować odczytową projekcję
`digital-twin[name="self"]` z allowlistą pól, redakcją, rendererem i odbiorcami
rolowymi. W Subactor należy używać `authorization: aql+subject`: DOQL opisuje
widok, a zweryfikowana tożsamość i AQL wymuszają odczyt wyłącznie własnego
podmiotu. Przykład znajduje się w `examples/digital-twin-self.doql.css`.
Helper `project_self_view()` dla `authorization: aql+subject` wymaga jawnego
`aql_authorized=True` oraz `audit_sink`. Projekcja kopiuje wyłącznie pola z
allowlisty, rekursywnie usuwa sekretne klucze i odrzuca cykle, wartości
nieserializowalne oraz zbyt duże struktury.


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-1.0.44-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$7.74-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-63.0h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $7.7445 (75 commits)
- 👤 **Human dev:** ~$6301 (63.0h @ $100/h, 30min dedup)

Generated on 2026-09-03 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

![Version](https://img.shields.io/badge/version-1.0.44-blue) ![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green) ![Status](https://img.shields.io/badge/status-stable-green)



---

**Data wydania:** 2026-04-20  
**Wersja:** 1.0.0 (stable)  
**Zawartość:** repo `doql/` + repo `articles/` + ten README  
**Zmiany:** CSS-like syntax, redeploy integration, public API `__all__`

---

## Do czego można użyć doql

**doql (Declarative OQL)** to generator deklaratywny, który z jednego pliku `.doql` tworzy kompletne aplikacje, dokumenty i integracje. Zamiast pisać kod — deklarujesz **co** ma powstać, a generator robi **jak**.

### 10 głównych zastosowań

| # | Zastosowanie | Co powstaje | Przykład w repo |
|---|--------------|-------------|-----------------|
| 1 | **Aplikacje SaaS** | Full-stack: API + Web + Mobile + Desktop | `examples/asset-management/` — klon Drägerware dla BHP |
| 2 | **Laboratoria kalibracyjne** | System ISO 17025 z 4-eyes, WORM, świadectwami | `examples/calibration-lab/` — lab z zarządzaniem wzorcami |
| 3 | **Flota IoT** | Zarządzanie urządzeniami, OTA, monitoring Prometheus | `examples/iot-fleet/` — flota Raspberry Pi z mapą |
| 4 | **Generowanie dokumentów** | PDF, HTML, DOCX bez backendu | `examples/document-generator/` — świadectwa kalibracyjne |
| 5 | **Stanowiska kiosk** | Tablety/Raspberry Pi w trybie fullscreen | `examples/kiosk-station/` — operator panel na hali |
| 6 | **Prototypy full-stack** | API + web + mobile + desktop z jednego pliku | `examples/notes-app/` — notatnik wszystkie platformy |
| 7 | **Aplikacje PWA** | Mobile-first, offline, installable | `examples/todo-pwa/` — minimalna lista zadań |
| 8 | **Systemy CMS** | Blogi, treści, tagi, komentarze | `examples/blog-cms/` — prosty blog |
| 9 | **CRM i pipeline** | Kontakty, leady, sprzedaż | `examples/crm-contacts/` — zarządzanie klientami |
| 10 | **Sklepy e-commerce** | Koszyk, zamówienia, płatności | `examples/e-commerce-shop/` — sklep online |

### Co generuje doql z jednej deklaracji

- **API** — FastAPI, OpenAPI, SDK TypeScript
- **Web** — React + Vite, responsywny UI
- **Mobile** — PWA (Progressive Web App)
- **Desktop** — Tauri v2 (Rust-based, lightweight)
- **Dokumenty** — PDF, HTML, Markdown, DOCX
- **Bazy danych** — SQLite, PostgreSQL ze schematem
- **Infrastruktura** — Docker, Kubernetes, Terraform, Nginx, systemd
- **CI/CD** — GitHub Actions, GitLab CI, Jenkins pipeline
- **Testy** — Scenariusze `.testql.toon.yaml` z integracją hardware

### Formaty deklaracji

```bash
app.doql          # YAML-like, indentacja
app.doql.css      # CSS-like: entity[name="X"] { ... }
app.doql.less     # CSS + zmienne @primary
app.doql.sass     # SASS + zmienne $primary
```

Wszystkie formaty są równoważne — możesz konwertować między nimi.

---

## Co jest w tej paczce

### `doql/` — nowy projekt: generator deklaratywny
Kompletny projekt **doql** — warstwa deklaratywna nad `oqlos`, która z jednego pliku `.doql` generuje aplikacje, dokumenty, kioski, integracje API. Licencja Apache 2.0 (open core).

**Kluczowe dokumenty:**
- `README.md` — wprowadzenie, quick start, link do wszystkich sekcji
- `SPEC.md` — pełna specyfikacja języka v0.2.3 (21 sekcji, wszystkie typy artefaktów)
- `GLOSSARY.md` — **jednoznaczna semantyka OQL / DOQL / IQL** (niezbędne, jeśli komunikujesz projekt publicznie)
- `OQLOS-REQUIREMENTS.md` — lista zmian w oqlos (8 wymagań: 5 krytycznych, 3 dodane przy v0.2)
- `ROADMAP.md` — fazy 0-3 rozwoju, ~8 tygodni do produkcji
- `CHANGELOG.md` — historia wersji v0.1 i v0.2

**Dziesięć przykładów (gotowych `.doql` / `.doql.css` / `.doql.less` / `.doql.sass`):**
- `examples/asset-management/` — klon Drägerware, pełen SaaS dla BHP (`.doql` + `.doql.css`)
- `examples/calibration-lab/` — laboratorium ISO 17025 z 4-eyes i WORM (`.doql` + `.doql.less`)
- `examples/iot-fleet/` — flota RPi z OTA canary i Prometheus (`.doql` + `.doql.less`)
- `examples/document-generator/` — generator PDF bez backendu (`.doql` + `.doql.less`)
- `examples/kiosk-station/` — stanowisko operatora na tablecie (`.doql` + `.doql.css`)
- `examples/notes-app/` — full-stack demo: API + web + mobile + desktop (`.doql` + `.doql.sass`)
- `examples/todo-pwa/` — minimalna aplikacja PWA mobile-first (`.doql` + `.doql.css`)
- `examples/blog-cms/` — prosty blog CMS z tagami i komentarzami (`.doql.sass`)
- `examples/crm-contacts/` — kontakty CRM z pipeline sprzedaży (`.doql.less`)
- `examples/e-commerce-shop/` — sklep e-commerce z koszykiem i zamówieniami (`.doql.css`)

**Infrastruktura projektu:**
- `pyproject.toml` — pakowanie Python
- `doql/cli/` — CLI z 21 komendami: init/validate/plan/build/run/deploy/sync/export/import/generate/render/query/kiosk/quadlet/docs/adopt/doctor/drift/workspace/publish
- `doql/parsers/` — parser classic `.doql` + CSS-like parser (`.doql.css`, `.doql.less`, `.doql.sass`)
- `doql/exporters/` — eksport do YAML, Markdown, CSS/LESS/SASS
- `doql/importers/` — import z YAML do `.doql`
- `doql/generators/` — generatory: API, Web, Mobile, Desktop, Infra (docker-compose, K8s, Terraform, Nginx, Quadlet, Kiosk), Documents, Reports, i18n, Workflow, CI (GitHub, GitLab, Jenkins)
- `doql/scaffolds/minimal/` — szablon dla `doql init` 
- `LICENSE` (Apache 2.0)
- `.gitignore` 

**Paczki tooling (`packages/*2doql`)** — mosty wejścia → DOQL (`.doql.less`). Pełny indeks: [`packages/README.md`](packages/README.md).

| Pakiet | Do czego służy | README |
|--------|----------------|--------|
| **mcp2doql** | Serwer MCP (stdio) — query/patch/validate/DSL przez narzędzia MCP | [`packages/mcp2doql/README.md`](packages/mcp2doql/README.md) |
| **cli2doql** | Shell CLI (REPL) sterujący DOQL przez DSL (`dsl2doql`) | [`packages/cli2doql/README.md`](packages/cli2doql/README.md) |
| **dsl2doql** | DSL sterowania DOQL (QUERY, PATCH, VALIDATE, ADOPT, …) | [`packages/dsl2doql/README.md`](packages/dsl2doql/README.md) |
| **nlp2doql** | Sterowanie DOQL przez NL (generate, apply, edit) | [`packages/nlp2doql/README.md`](packages/nlp2doql/README.md) |
| **uri2doql** | `doql://` URI — query, patch, apply, nlp2uri | [`packages/uri2doql/README.md`](packages/uri2doql/README.md) |

Skanowanie MCP/CLI (adopt) i konwersja OQL→workflow są w **`doql/`**: `doql/adopt/scanner/interfaces/{mcp,cli}.py`, `doql/importers/oql_converter.py`.

Instalacja dev (wszystkie paczki workspace):

```bash
uv sync --extra deploy
# lub: pip install -e ".[dev]" -e packages/mcp2doql -e packages/cli2doql ...
```

### `articles/` — artykuły WordPress
Sześć artykułów markdown z YAML front-matter gotowych do publikacji (kompatybilne z `wp-cli` i WordPress REST API). Każdy artykuł to jeden projekt / jedna nowość.

**Lista:**
1. `01-oqlos-status-2026-q2.md` — status oqlos po refaktorze (CC̄ 3,7→3,2)
2. `02-testql-status-2026-q2.md` — TestQL, porównanie z Playwright
3. `03-saas-www-status-2026-q2.md` — SaaS oqlos.com, 5 bugów P0, diagnoza landingu
4. `04-doql-ogloszenie.md` — ogłoszenie doql v0.1 (SaaS generator)
5. `05-wizja-ekosystemu-oqlos.md` — wizja całej rodziny (4 warstwy, strategia open-core)
6. `06-doql-v02-dokumenty-kiosk.md` — doql v0.2 (dokumenty, kiosk, semantyka)

Każdy 800-1800 słów, po polsku, gotowy do kopiuj-wklej do WordPressa.

---

## Jak to odpalić

### Instalacja doql (po sklonowaniu do repo)

```bash
cd doql/
pip install -e .
doql --version
```

### Przykłady użycia CLI

#### Inicjalizacja nowego projektu

```bash
# Utwórz nowy projekt z szablonu
doql init my-app --template minimal
cd my-app

# Lista dostępnych szablonów
doql init - --list-templates
```

#### Reverse-engineer istniejącego projektu

```bash
# Zeskanuj istniejący projekt → app.doql.less
doql adopt ./my-project --force

# Zeskanuj zdalne urządzenie przez SSH
doql adopt --from-device pi@kiosk-01.local --format css

# Zbuduj w innym folderze
cp app.doql.less /tmp/rebuild/
cd /tmp/rebuild
doql build --force
```

#### Minimalny przykład — Todo PWA

```bash
cd examples/todo-pwa
doql validate                    # sprawdź deklarację
doql plan                        # podgląd co zostanie wygenerowane
doql build                       # generuj kod
doql run -t api                 # uruchom API na http://localhost:8000
doql run -t mobile              # uruchom PWA na http://localhost:8091
```

#### Asset Management — pełen stack (API + Web + Mobile + Desktop)

```bash
cd examples/asset-management
cp .env.example .env
doql validate
doql build

doql run -t api        # FastAPI → http://localhost:8000/docs
doql run -t web        # React   → http://localhost:5173
doql run -t mobile     # PWA     → http://localhost:8091
doql run -t desktop    # Tauri desktop app (wymaga Rust)
doql run               # pełny stack via docker-compose
```

#### Laboratorium kalibracyjne ISO 17025

```bash
cd examples/calibration-lab
doql validate
doql build
doql run -t api        # FastAPI → http://localhost:8000/docs
doql run -t web        # React   → http://localhost:5173
```

#### Generator PDF (świadectwa kalibracyjne)

```bash
cd examples/document-generator
cp .env.example .env
doql validate
doql build
doql run -t web        # htmx UI → http://localhost:8080

# Generowanie pojedynczego dokumentu (nazwa musi pasować do DOCUMENT w pliku .doql):
doql generate calibration_certificate
```

#### CRM Contacts

```bash
cd examples/crm-contacts
doql validate
doql build
doql run -t api        # FastAPI → http://localhost:8000/docs
doql run -t web        # React   → http://localhost:5173
```

#### IoT Fleet Manager (Kubernetes)

```bash
cd examples/iot-fleet
doql validate
doql build
doql run -t api        # FastAPI → http://localhost:8000/docs
doql run -t web        # React + Leaflet map → http://localhost:5173
```

#### Kiosk Station (Raspberry Pi)

```bash
cd examples/kiosk-station
doql validate
doql build

# Instalacja na urządzeniu:
scp -r build/infra pi@kiosk-01.local:/tmp/
ssh pi@kiosk-01.local "sudo /tmp/infra/install-kiosk.sh && sudo reboot"
```

#### Deployment via redeploy (v1.0+)

```bash
# Instaluj z opcjonalnym deploy support
cd examples/asset-management
pip install "doql[deploy]>=1.0.0"

# Build generuje migration.yaml
doql build

# Deploy do środowiska dev (wymaga redeploy>=0.2.0)
doql deploy --env dev

# Deploy do Podman Quadlet (rootless)
doql quadlet --install
```

#### Synchronizacja zmian (merge-friendly)

```bash
# Re-generuj tylko zmienione części (bez nadpisywania ręcznych zmian)
doql sync

# Synchronizacja w innym katalogu
doql -d examples/asset-management sync
```

#### Eksport do innych formatów

```bash
# Eksport specyfikacji do CSS
doql export --format css -o spec.doql.css

# Eksport do LESS ze zmiennymi
doql export --format less -o spec.doql.less

# Eksport do SASS
doql export --format sass -o spec.doql.sass

# Eksport OpenAPI spec
doql export --format openapi -o openapi.yaml

# Eksport Postman collection
doql export --format postman -o collection.json

# Eksport TypeScript SDK
doql export --format typescript-sdk -o sdk/

# Eksport dokumentacji Markdown
doql export --format markdown -o docs/

# Eksport YAML
doql export --format yaml -o spec.yaml
```

#### Import z YAML

```bash
# Import YAML → .doql
doql import spec.yaml --format css -o app.doql.css

# Import z konwersją do LESS
doql import spec.yaml --format less -o app.doql.less
```

#### Generowanie pojedynczych artefaktów

```bash
# Generuj pojedynczy dokument (nazwa musi pasować do DOCUMENT w pliku .doql)
doql generate calibration_certificate

# Generuj raport
doql generate monthly_report
```

#### Renderowanie szablonów

```bash
# Renderuj szablon z danymi
doql render templates/invoice.jinja2
```

#### Query — zapytania do źródeł danych

```bash
# Zapytaj źródło danych i zwróć JSON
doql query customer_db

# Z zapytaniem w kontekście innym niż CWD
doql -d examples/asset-management query devices
```

#### Kiosk — zarządzanie urządzeniami kiosk

```bash
# Instalacja kiosk na obecnym urządzeniu (Raspberry Pi)
doql kiosk --install

# Zbuduj i zainstaluj
cd examples/kiosk-station
doql build && doql kiosk --install
```

#### Quadlet — Podman rootless

```bash
# Instalacja Quadlet do systemd (rootless)
doql quadlet --install

# Sprawdź status
doql doctor --env local
```

#### Dokumentacja

```bash
# Generuj stronę dokumentacji z projektu
doql docs

# Zapisz do konkretnego folderu
doql docs && cp -r build/docs /var/www/html/
```

#### Diagnostyka projektu

```bash
# Diagnostyka lokalnego projektu
doql doctor

# Diagnostyka zdalnego środowiska
doql doctor --env staging

# Napraw automatycznie wykryte problemy
doql doctor --fix
```

#### Drift — porównanie z rzeczywistością

```bash
# Porównaj deklarację ze stanem zdalnego urządzenia
doql drift --from-device pi@kiosk-01.local

# Wyjście JSON (machine-readable)
doql drift --from-device pi@kiosk-01.local --json

# Porównanie z konkretnym plikiem
doql drift --from-device pi@kiosk-01.local --file app.doql.less
```

#### Publikacja artefaktów

```bash
# Publikuj wszystko (PyPI, npm, Docker, GitHub)
doql publish

# Tylko wybrane targety
doql publish --target pypi,docker

# Symulacja (dry-run)
doql publish --dry-run
```

#### Uwaga: `doql run` vs `doql -d ... run`

```bash
# z katalogu projektu — krótsza forma:
cd examples/asset-management
doql run -t desktop

# z dowolnego miejsca — z flagą -d:
doql -d examples/asset-management run -t desktop
doql -d examples/notes-app run -t web
```

### Szybki start z CLI shell (alternatywa)

```bash
# Generuj i uruchom desktop app
./doql.sh examples/notes-app/app.doql desktop

# Generuj i uruchom web
./doql.sh examples/notes-app/app.doql web

# Generuj wszystko
./doql.sh examples/notes-app/app.doql all
```

### `doql workspace` — operacje na wielu projektach

Gdy trzymasz kilka projektów z `app.doql.css` w jednym folderze (np. `~/github/oqlos/`), `doql workspace` pozwala na grupowe operacje.

```bash
# Wylistuj wszystkie projekty z app.doql.css (głębokość 2)
doql workspace list --root ~/github/oqlos --depth 2

# Przeanalizuj wszystkie projekty: workflowy, entity, bazy, interfejsy
doql workspace analyze --root ~/github/oqlos

# Eksport do CSV (do arkusza / BI / raportu)
doql workspace analyze --root ~/github/oqlos -o oqlos_report.csv

# Walidacja manifestów (puste workflowy, brak sekcji app{}, itp.)
doql workspace validate --root ~/github/oqlos
doql workspace validate --root ~/github/oqlos --strict   # exit 1 przy błędach

# Filtrowanie po obecności workflowa
doql workspace list --root ~/github/oqlos --has-workflow test

# Uruchomienie `doql <action>` we wszystkich projektach
doql workspace run validate --root ~/github/oqlos --dry-run
doql workspace run validate --root ~/github/oqlos
doql workspace run build    --root ~/github/oqlos --fail-fast

# Naprawa błędów w manifestach (wymaga `pip install taskfile`)
doql workspace fix --root ~/github/oqlos --dry-run
doql workspace fix --root ~/github/oqlos
```

Podstawowa pętla (list/analyze/validate/run) działa bez dodatkowych zależności.
Komenda `fix` używa `taskfile.workspace` do napraw (puste workflowy, orphans,
brakujące workflowy z Taskfile.yml) — zainstaluj `pip install taskfile`, aby
odblokować.

Pełna dokumentacja i równoważna komenda `taskfile workspace`: zob.
[`pyfunc/taskfile/docs/WORKSPACE.md`](../../pyfunc/taskfile/docs/WORKSPACE.md).

### Publikacja artykułów

Opcja A — ręcznie do WP (najprostsze):
1. Skopiuj treść pliku `.md` bez front-matter
2. Wklej w edytorze WordPress (tryb Markdown jeśli masz plugin)
3. Tytuł, slug, kategorie, tagi z YAML front-matter

Opcja B — `wp-cli`:
```bash
for file in articles/*.md; do
  # yq wyciąga pola z front-matter, sed wycina YAML z body
  title=$(yq -r '.title' "$file")
  slug=$(yq -r '.slug' "$file")
  body=$(sed '/^---$/,/^---$/d' "$file")
  wp post create --post_title="$title" --post_name="$slug" \
    --post_content="$body" --post_status=publish
done
```

Opcja C — GitHub Action z WP REST API (plik `.github/workflows/publish.yml` — nie dołączony, łatwo dopisać).

---

## Formaty plików `.doql`

doql obsługuje cztery równoważne formaty specyfikacji:

| Format | Rozszerzenie | Styl |
|--------|-------------|------|
| Classic | `.doql` | indentacja YAML-like |
| CSS | `.doql.css` | `entity[name="X"] { ... }` |
| LESS | `.doql.less` | CSS + zmienne `@var` |
| SASS | `.doql.sass` | CSS + zmienne `$var`, indent-based |

Wszystkie formaty parsują się do tego samego `DoqlSpec` — można mieszać w projekcie i konwertować:

```bash
# Eksport do innego formatu
doql export --format less -o spec.doql.less

# Import z YAML
doql import spec.yaml --format css -o app.doql
```

Każdy example zawiera zarówno wersję `.doql` jak i wersję CSS-like (`.doql.css` / `.doql.less` / `.doql.sass`).

---

## Architektura — jak się to wszystko łączy

```
┌─────────────────────────────────────────────┐
│   doql file (.doql / .doql.css / .less / …) │
│   deklaracja CO ma powstać                  │
└──────────────┬──────────────────────────────┘
               │  doql build
               ▼
   ┌───────────┴───────────┬──────────────┬─────────────┐
   ▼                       ▼              ▼             ▼
 ┌────┐   ┌────┐   ┌──────────┐   ┌────────┐   ┌──────────┐
 │API │   │Web │   │ Mobile/  │   │Kiosk   │   │Documents │
 │    │   │    │   │ Desktop  │   │        │   │PDF/HTML  │
 └─┬──┘   └────┘   └──────────┘   └────────┘   └──────────┘
   │
   │ wywołuje scenariusze .oql
   ▼
 ┌────────────────────────────────────┐
 │ oqlos runtime (interpretuje .oql)  │
 └──────────────┬─────────────────────┘
                │ Modbus / MQTT / USB / GPIO
                ▼
         ┌────────────┐
         │  Hardware  │
         └────────────┘
```

Testy aplikacji (`.testql.toon.yaml`) → testql → Playwright-alternative z integracją hardware.

---

## Co dalej

**Zrealizowane (Fazy 0–4):**
- ✅ Parser `.doql` v0.2.3 (21 sekcji) + CSS-like parser (`.doql.css` / `.doql.less` / `.doql.sass`)
- ✅ 10 przykładów z walidacją i budowaniem
- ✅ Generatory: API (FastAPI), Web (React+Vite), Mobile (PWA), Desktop (Tauri v2), Infra (docker-compose, K8s, Terraform, Nginx, Quadlet, Kiosk), Documents, Reports, CI (GitHub, GitLab, Jenkins)
- ✅ Plugin system + 4 pluginy (GxP, ISO17025, Fleet, ERP)
- ✅ Eksport/Import: YAML, Markdown, CSS/LESS/SASS, OpenAPI, Postman, TypeScript SDK
- ✅ LSP server dla VS Code + playground online (Pyodide)
- ✅ `doql adopt` — reverse-engineer istniejącego projektu → app.doql.css
- ✅ `doql doctor` — diagnostyka projektu + remote SSH checks
- ✅ `doql build --no-overwrite` — merge-friendly build
- ✅ Deploy directives `@local`/`@push`/`@remote` w bloku deploy
- ✅ `doql publish` — PyPI, npm, Docker, GitHub releases
- ✅ 130 testów pytest, CI matrix 3.10–3.13

**Następne kroki:**
- Certyfikacja deweloperów (`Doql Certified Developer`)
- Parser tree-sitter (pełna gramatyka, error recovery)
- Rozszerzenie VS Code o wsparcie `.doql.css` / `.doql.less` / `.doql.sass`
- Pilot w realnej firmie (lab kalibracyjny w Gdańsku)

**Q3-Q4:**
- Marketplace szablonów `.doql` 
- Premium plugins (GxP, ISO 17025, Fleet)
- Walidacja drugiego segmentu ICP (pharma / medtech)

---

## Licencja

- **doql** i wszystkie jego przykłady — Apache 2.0
- **articles** — CC BY 4.0 (można cytować i tłumaczyć z atrybucją)

Premium plugins doql (komercyjne) — osobne warunki, patrz `doql/LICENSE`.

---

## Kontakt

- Repo główne: github.com/softreck/oqlos
- Repo doql: github.com/softreck/doql
- Email: hello@softreck.dev


## License

Licensed under Apache-2.0.
## Architecture
