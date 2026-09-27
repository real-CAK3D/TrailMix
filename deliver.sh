#!/usr/bin/env bash
# After Maple files Trail Mix: print the issue and ring The Corner Chronicle's bell.
set -u
D="$HOME/.hermes/garden/trail-mix"; PY="$HOME/.hermes/hermes-agent/venv/bin/python"; M=$(TZ=America/New_York date +%Y-%m)
F="$D/drafts/$M.json"; [ -f "$F" ] || { echo "no Trail Mix draft for $M"; exit 0; }
cd "$D" && "$PY" render_trail.py "$F" || exit 1
HEAD=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]))["cover"]["title"])' "$F" 2>/dev/null)
"$PY" "$HOME/.hermes/garden/newsstand/notify.py" "🥾 Trail Mix is out" "${HEAD:-Maple and Herbie's new issue}" "/trail-mix/"
