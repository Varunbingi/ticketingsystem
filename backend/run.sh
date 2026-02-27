#!/usr/bin/env bash
set -euo pipefail
# run.sh - simple helper to run the backend using the local .venv
# Usage: ./run.sh

cd "$(dirname "$0")"

if [ -f .venv/bin/activate ]; then
  # prefer to activate so that uvicorn/other console tools are available on PATH
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m uvicorn main:app --reload
else
  echo ".venv not found in backend/. Use .venv/bin/python -m uvicorn main:app --reload instead."
  exit 1
fi
