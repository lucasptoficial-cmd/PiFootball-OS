#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LICENSE="$ROOT/apps/picraft/THIRD_PARTY_LICENSE.txt"

echo "=============================================="
echo " PiCraft — instalação do motor Python Edition"
echo "=============================================="
echo
echo "CRITÉRIOS DE COMPATIBILIDADE"
echo "- Raspberry Pi OS/Debian 32-bit ARMv7: experimental, sem garantia."
echo "- Raspberry Pi 2 (1 GB RAM): abaixo do recomendado; compilação pode falhar."
echo "- Python 3.9 ou superior."
echo "- OpenGL funcional e ambiente gráfico X11/Wayland."
echo "- Internet necessária para descarregar dependências."
echo "- Dependências do motor: Pyglet 1.5.x, Cython, Pillow, NumPy,"
echo "  PyOgg e nbtlib. wxPython é opcional."
echo "- O motor original usa extensões Cython; a compilação em ARMv7"
echo "  pode não ser suportada ou consumir demasiada memória."
echo
echo "LICENÇA DO MOTOR DE TERCEIROS — BSD 3-CLAUSE"
cat "$LICENSE"
echo
echo "Ao continuar, confirmas que leste e aceitas os termos BSD acima."
read -r -p "Aceitas a licença e queres continuar? [s/N] " ACCEPT
case "$ACCEPT" in
  s|S|sim|SIM) ;;
  *) echo "Instalação cancelada. Nenhuma dependência do PiCraft foi instalada."; exit 0 ;;
esac

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Erro: Python 3 não encontrado."; exit 1
fi
"$PYTHON" - <<'PY'
import sys
if sys.version_info < (3, 9):
    raise SystemExit("Erro: o motor requer Python 3.9 ou superior.")
print("Python:", sys.version.split()[0])
PY

ARCH="$(uname -m)"
echo "Arquitetura detetada: $ARCH"
if [ "$ARCH" = "armv7l" ] || [ "$ARCH" = "armv6l" ]; then
  echo "AVISO: ARM 32-bit é experimental para este motor."
fi
if [ -r /proc/meminfo ]; then
  awk '/MemTotal/ {printf "RAM detetada: %.0f MB\\n", $2/1024}' /proc/meminfo
fi
echo
echo "A instalação automática das dependências do motor ainda não é"
echo "executada neste passo: valida primeiro a compatibilidade do sistema."
echo "Consulta apps/picraft/README-INSTALACAO.md antes de compilar."
