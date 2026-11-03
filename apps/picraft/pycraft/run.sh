#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m pip install --user -r requirements.txt
exec python3 main.py
