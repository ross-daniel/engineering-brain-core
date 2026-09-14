#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
mkdir -p .context-packs

echo "Vault root: $ROOT"
echo

for cmd in git python3 claude obsidian; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd: $(command -v "$cmd")"
  else
    echo "NOTE: '$cmd' not found on PATH."
  fi
done

echo
cat <<'TXT'
Recommended machine-local shell configuration (adapt paths to your machine):

  export BRAIN_ROOT="$HOME/Documents/Your-Brain"
  export BRAIN_CORE_ROOT="$HOME/Documents/engineering-brain-core"
  export CODE_ROOT="$HOME/Desktop/Codebases"

  cbrain() {
      claude --add-dir "$BRAIN_ROOT" "$@"
  }

Optional external storage can use a vault-specific alias defined in
99_System/Machine Setup.md.

Core update check:
  ./99_System/Scripts/update-brain-core.sh --dry-run

Zotero metadata check:
  python3 99_System/Scripts/refresh-zotero.py

For Zotero, keep Zotero desktop running and enable:
Settings -> Advanced -> Allow other applications on this computer to
communicate with Zotero.
TXT
