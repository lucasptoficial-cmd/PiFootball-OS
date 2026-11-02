#!/usr/bin/env bash
set -euo pipefail
if ! command -v apt-get >/dev/null 2>&1; then
  echo 'Este instalador requer Raspberry Pi OS ou Debian com apt.'
  exit 1
fi
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-pygame python3-cec cec-utils git
echo 'Dependências instaladas. Executa: bash scripts/run.sh'
