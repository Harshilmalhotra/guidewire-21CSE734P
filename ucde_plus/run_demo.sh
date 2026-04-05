#!/usr/bin/env bash
set -e

echo "[UCDE++] Executing Initialization Sequence..."

# 1. Validate Python Bounds
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python3 is inherently required natively. Aborting execution loops."; exit 1; }

echo "[UCDE++] Installing dependencies securely mapped within isolated virtual architectures..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "[UCDE++] Restoring Database Constraints Native Demo Seed Mappings..."
python reset_demo.py

echo "[UCDE++] Launching Uvicorn FastApi Native Interface Server limits cleanly bound on 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000

echo "[UCDE++] Initialization Concluded."
