#!/usr/bin/env bash
# End-to-end runtime deployment smoke test.
# Builds, launches the generated API, runs tests, and cleans up.
set -eo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="/tmp/doql-runtime"
API_DIR="$ROOT/examples/asset-management/build/api"
DOQL_BIN="$ROOT/venv/bin/doql"
if [[ ! -x "$DOQL_BIN" ]]; then
  DOQL_BIN="$(command -v doql)"
fi
PORT=8766
LOG=/tmp/doql-api.log
PIDFILE=/tmp/doql-api.pid

cleanup() {
  if [[ -f "$PIDFILE" ]]; then
    local pid
    pid=$(cat "$PIDFILE")
    kill "$pid" 2>/dev/null || true
    rm -f "$PIDFILE"
  fi
  # Kill any lingering uvicorn on our port (safety net)
  pkill -f "uvicorn main:app.*--port $PORT" 2>/dev/null || true
}
trap cleanup EXIT

# 1. Fresh build
echo "=== Building ==="
"$DOQL_BIN" -d "$ROOT/examples/asset-management" build --force 2>&1 | tail -3

# 2. Clear DB
rm -f "$API_DIR/data.db"

# 3. Launch server
cd "$API_DIR"
JWT_SECRET=test-secret "$VENV/bin/uvicorn" main:app \
    --host 127.0.0.1 --port $PORT > "$LOG" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PIDFILE"
echo "Server launched pid=$SERVER_PID"

# 4. Wait for /health
for i in $(seq 1 40); do
  sleep 0.25
  if curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    echo "✓ Server ready after ${i}×250ms"
    break
  fi
  if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "✗ Server died during startup — log:"
    tail -30 "$LOG"
    exit 1
  fi
done

if ! curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
  echo "✗ Server never became healthy — log:"
  tail -30 "$LOG"
  exit 1
fi

# 5. Run smoke tests
echo ""
"$VENV/bin/python" "$ROOT/tests/runtime_smoke.py"
RESULT=$?

exit $RESULT
