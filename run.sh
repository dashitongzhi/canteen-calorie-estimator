#!/usr/bin/env bash
# Quickstart: ./run.sh  (requires Python 3.10+)
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000
