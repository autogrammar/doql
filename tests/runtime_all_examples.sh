#!/usr/bin/env bash
# Boot every example's generated API and verify /health + OpenAPI responds.
# Catches regressions across all generator paths, not just asset-management.
set -eo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="/tmp/doql-runtime"
PORT=8777
DOQL_BIN="$ROOT/venv/bin/doql"
if [[ ! -x "$DOQL_BIN" ]]; then
  DOQL_BIN="$(command -v doql)"
fi

# All ten showcase examples.  Those without api/main.py (document-generator,
# kiosk-station) are automatically skipped by the loop below.
EXAMPLES=(
  asset-management
  blog-cms
  calibration-lab
  crm-contacts
  document-generator
  e-commerce-shop
  iot-fleet
  kiosk-station
  notes-app
  todo-pwa
)

# Ensure runtime venv has all API deps (idempotent).
if [[ -x "$VENV/bin/pip" ]]; then
  "$VENV/bin/pip" install -q python-multipart 2>/dev/null || true
fi

cleanup() {
  pkill -f "uvicorn main:app.*--port $PORT" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

pass=0
skip=0
fail=0

for ex in "${EXAMPLES[@]}"; do
  api_dir="$ROOT/examples/$ex/build/api"
  printf "\n── %-22s  " "$ex"

  # Ensure fresh build
  "$DOQL_BIN" -d "$ROOT/examples/$ex" build --force >/dev/null 2>&1 || {
    echo "✗ build failed"; fail=$((fail+1)); continue
  }

  if [[ ! -f "$api_dir/main.py" ]]; then
    echo "— (no API generated, skipped)"
    skip=$((skip+1))
    continue
  fi

  # Skip examples that hardcode postgresql:// when psycopg2 is not installed
  if grep -q 'postgresql://' "$api_dir/database.py" 2>/dev/null; then
    if ! "$VENV/bin/python" -c "import psycopg2" 2>/dev/null; then
      echo "— (postgres required, psycopg2 absent, skipped)"
      skip=$((skip+1))
      continue
    fi
  fi

  # Compile the API as a sanity check (catches syntax errors)
  py_files=()
  for f in main.py routes.py models.py schemas.py auth.py; do
    [[ -f "$api_dir/$f" ]] && py_files+=("$f")
  done
  (cd "$api_dir" && "$VENV/bin/python" -m py_compile "${py_files[@]}") || {
    echo "✗ .py compile failed"; fail=$((fail+1)); continue
  }

  # Boot server
  mkdir -p "$api_dir/data"
  rm -f "$api_dir/data"/*.db "$api_dir/data.db"
  cleanup; sleep 0.3
  (cd "$api_dir" && JWT_SECRET=test-secret DATABASE_URL=sqlite:///./data/app.db \
    "$VENV/bin/uvicorn" main:app \
    --host 127.0.0.1 --port $PORT > /tmp/doql-ex-${ex}.log 2>&1) &
  server_pid=$!

  # Wait
  ready=0
  for i in $(seq 1 40); do
    sleep 0.25
    if curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      ready=1
      break
    fi
    kill -0 $server_pid 2>/dev/null || break
  done

  if [[ $ready -eq 0 ]]; then
    echo "✗ did not become ready"
    tail -5 /tmp/doql-ex-${ex}.log | sed 's/^/        /'
    fail=$((fail+1))
    kill $server_pid 2>/dev/null || true
    continue
  fi

  # Verify OpenAPI schema
  endpoints=$(curl -sf "http://127.0.0.1:$PORT/openapi.json" | \
    "$VENV/bin/python" -c "import sys,json; print(len(json.load(sys.stdin)['paths']))")
  echo "✓ /health OK  |  $endpoints endpoints"

  kill $server_pid 2>/dev/null || true
  wait $server_pid 2>/dev/null || true
  pass=$((pass+1))
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  passed: $pass    skipped: $skip    failed: $fail"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $fail
