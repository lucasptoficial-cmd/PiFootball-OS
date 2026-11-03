#!/usr/bin/env bash
set -euo pipefail
if ! command -v apt-get >/dev/null 2>&1; then
  echo 'Este instalador requer Raspberry Pi OS ou Debian com apt.'
  exit 1
fi
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-pygame python3-cec cec-utils git
echo
echo 'Pretendes ver/instalar o motor PiCraft Python Edition?'
echo 'O instalador apresenta a licença BSD-3-Clause e verifica os critérios.'
read -r -p 'Executar instalador do PiCraft? [s/N] ' PICRAFT
case "$PICRAFT" in
  s|S|sim|SIM) bash "$(dirname "$0")/install_picraft.sh" ;;
  *) echo 'PiCraft ignorado; instalação do PiFootball OS concluída.' ;;
esac
echo 'Dependências base instaladas. Executa: bash scripts/run.sh'
