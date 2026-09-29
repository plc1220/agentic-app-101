#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Install Python 3.11 or newer, then run: bash run.sh"
  exit 1
fi
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Python 3.11 or newer is required by Deep Agents.")'
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env. Add your Gemini key, then run: bash run.sh"
  echo "For an offline walkthrough, set AGENT_MODE=sample instead."
  exit 1
fi
if [ ! -x .venv/bin/python ]; then python3 -m venv .venv; fi
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python launch.py
