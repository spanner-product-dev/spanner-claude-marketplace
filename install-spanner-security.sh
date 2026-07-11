#!/usr/bin/env bash
# install-spanner-security.sh
# Pins the Spanner security plugin ON for Claude Code via managed settings (no MDM).
# Managed settings live at a system path, so this needs admin (sudo).
#
# One-liner (teammates run this once):
#   curl -fsSL https://raw.githubusercontent.com/spanner-product-dev/spanner-claude-marketplace/main/install-spanner-security.sh | sudo bash
#
# Then fully quit and reopen Claude Code.
set -euo pipefail

# Re-run with sudo if not already root (skipped when invoked via `sudo bash`).
if [ "$(id -u)" -ne 0 ]; then
  echo "This writes a system policy file and needs admin. Re-running with sudo…"
  exec sudo bash "$0" "$@"
fi

DIR="/Library/Application Support/ClaudeCode"
FILE="$DIR/managed-settings.json"
mkdir -p "$DIR"

# Merge our two keys into any existing managed-settings.json rather than overwriting it.
python3 - "$FILE" <<'PY'
import json, os, sys
path = sys.argv[1]
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        # Don't clobber an unreadable/invalid file silently — back it up first.
        os.rename(path, path + ".bak")
        print("Backed up existing invalid file to", path + ".bak")
        data = {}

mk = data.setdefault("extraKnownMarketplaces", {})
mk["spanner"] = {"source": {"source": "github",
                            "repo": "spanner-product-dev/spanner-claude-marketplace"}}
ep = data.setdefault("enabledPlugins", {})
ep["spanner-security@spanner"] = True
ep["spanner-toolkit@spanner"] = True

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print("Wrote", path)
PY

python3 -m json.tool "$FILE" >/dev/null && echo "valid JSON — OK"
echo "Done. Quit and reopen Claude Code, then run /plugin — spanner-security and spanner-toolkit should appear under 'Managed'."
