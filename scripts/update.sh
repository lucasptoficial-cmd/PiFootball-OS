#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Esta instalação não é uma cópia Git. Não é possível procurar atualizações."
  exit 0
fi
BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  echo "HEAD destacado; atualização automática cancelada."
  exit 0
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "Não existe remoto 'origin'."
  exit 0
fi
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "Existem alterações locais. Para proteger os teus ficheiros, não vou atualizar."
  echo "Guarda ou faz commit das alterações e tenta novamente."
  exit 0
fi

echo "A verificar atualizações do PiFootball OS..."
if ! git fetch --quiet origin "$BRANCH"; then
  echo "Não foi possível contactar o GitHub. Vou iniciar a versão instalada."
  exit 0
fi
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse FETCH_HEAD)"
if [ "$LOCAL" = "$REMOTE" ]; then
  echo "O PiFootball OS já está atualizado."
  exit 0
fi
if ! git merge-base --is-ancestor "$LOCAL" "$REMOTE"; then
  echo "A versão remota não é uma atualização direta. Atualização cancelada para evitar perda de dados."
  exit 0
fi
COUNT="$(git rev-list --count "$LOCAL..$REMOTE")"
echo "Está disponível uma atualização com $COUNT novo(s) commit(s)."
read -r -p "Queres atualizar agora? [s/N] " answer
case "$answer" in
  s|S|sim|SIM|Sim)
    gitdir="$(git rev-parse --git-dir)"
    printf '%s\n' "$LOCAL" > "$gitdir/pifootball-previous-commit"
    if git merge --ff-only "$REMOTE"; then
      echo "Atualização concluída. Podes voltar à versão anterior com: bash scripts/rollback.sh"
    else
      echo "A atualização falhou; a versão instalada não foi substituída."
      rm -f "$gitdir/pifootball-previous-commit"
    fi
    ;;
  *)
    echo "Sem alterações. Vou iniciar a versão atual."
    ;;
esac
