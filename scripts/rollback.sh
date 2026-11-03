#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Esta instalação não é uma cópia Git."
  exit 1
fi
gitdir="$(git rev-parse --git-dir)"
backup="$gitdir/pifootball-previous-commit"
if [ ! -s "$backup" ]; then
  echo "Ainda não existe uma versão anterior guardada por este atualizador."
  exit 1
fi
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "Existem alterações locais. Guarda-as primeiro; não vou apagá-las."
  exit 1
fi
PREVIOUS="$(cat "$backup")"
if ! git cat-file -e "$PREVIOUS^{commit}" 2>/dev/null; then
  echo "A versão anterior guardada já não está disponível."
  exit 1
fi
CURRENT="$(git rev-parse HEAD)"
echo "Versão atual:    $CURRENT"
echo "Versão anterior: $PREVIOUS"
read -r -p "Queres voltar à versão anterior? [s/N] " answer
case "$answer" in
  s|S|sim|SIM|Sim)
    git reset --hard "$PREVIOUS"
    printf '%s\n' "$CURRENT" > "$backup"
    echo "Regressaste à versão anterior. Podes repetir este comando para voltar à versão de onde vieste."
    ;;
  *)
    echo "Rollback cancelado."
    ;;
esac
