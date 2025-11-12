#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSION="${PYTHON_VERSION:-3.10.10}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "❌ $1 not found. Install it first."; exit 1; }; }

echo "🔎 Checking prerequisites..."
need asdf
need direnv
need uv

echo "👉 asdf: Python ${PYTHON_VERSION}"
asdf plugin add python >/dev/null 2>&1 || true
asdf install python "${PYTHON_VERSION}"
asdf set python "${PYTHON_VERSION}"
asdf reshim python

echo "👉 direnv: enabling python layout"
if ! grep -q "layout python" .envrc 2>/dev/null; then
  echo "layout python" >> .envrc
fi
direnv allow

echo "🔒 Locking deps (uv) -> requirements.txt"
uv pip compile pyproject.toml -o requirements.txt

echo "📦 Syncing env to requirements.txt"
uv pip sync requirements.txt

echo "🧹 Installing developer tools: Ruff + Mypy"
uv pip install ruff mypy

echo "🎭 Installing Playwright browsers"
python -m playwright install --with-deps

echo "✅ Done. Interpreter:"
python -c 'import sys; print(sys.executable)'
