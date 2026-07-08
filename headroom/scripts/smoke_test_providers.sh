#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTDIR="$ROOT/../headroom-state"
mkdir -p "$OUTDIR"

echo "Smoke-testing configured providers via running Headroom at http://127.0.0.1:8787"

curl -sS http://127.0.0.1:8787/readyz -o "$OUTDIR/proxy-readyz-smoke.txt" || true

probe() {
  model="$1"
  out="$OUTDIR/smoke_${model//[:\/]/_}.json"
  echo "Testing model: $model -> $out"
  curl -sS -X POST http://127.0.0.1:8787/v1/chat/completions \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"Say hello\"}]}" -m 60 > "$out" || true
}

# List of example models to probe (extend as you like)
probe "qwen2.5-coder:3b"
probe "qwen2.5-coder:1.5b"
probe "phi4-mini:latest"

echo "Smoke tests written to $OUTDIR (check smoke_*.json)"

