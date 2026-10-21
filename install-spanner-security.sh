#!/usr/bin/env bash
# install-spanner-security.sh
# Pins the Spanner security plugin ON for Claude Code via managed settings (no MDM).
# Managed settings live at a system path, so this needs admin (sudo).
#
# The repo is private, so raw.githubusercontent.com no longer serves this file. Teammates run it once,
# signed in to GitHub with the gh CLI (`gh auth login`, then `gh auth setup-git`):
#   gh api repos/spanner-product-dev/spanner-claude-marketplace/contents/install-spanner-security.sh -H "Accept: application/vnd.github.raw" | sudo bash
# or, from a clone of the repo:
#   sudo bash install-spanner-security.sh
#
# Then fully quit and reopen Claude Code.
set -euo pipefail

REPO="spanner-product-dev/spanner-claude-marketplace"

# Re-run with sudo if not already root (skipped when invoked via `sudo bash`).
if [ "$(id -u)" -ne 0 ]; then
  echo "This writes a system policy file and needs admin. Re-running with sudo…"
  exec sudo bash "$0" "$@"
fi

# Claude Code clones the marketplace with the signed-in user's own git credentials (SSH key, or gh's
# credential helper over HTTPS). Check that this Mac's user can read the private repo; warn, don't stop,
# because the policy file is still worth writing and access can be fixed afterwards.
USER_NAME="${SUDO_USER:-$(stat -f %Su /dev/console)}"
as_user() { sudo -H -u "$USER_NAME" "$@"; }
if as_user git ls-remote "https://github.com/$REPO.git" HEAD >/dev/null 2>&1 \
   || as_user ssh -o BatchMode=yes -o ConnectTimeout=5 -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
  echo "GitHub access for $USER_NAME — OK"
else
  echo "WARNING: $USER_NAME can't read github.com/$REPO yet, so Claude Code won't be able to load the plugin."
  echo "         Ask Mason for access to the spanner-product-dev org, then run: gh auth login && gh auth setup-git"
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
# autoUpdate: private marketplaces don't auto-update by default; the check uses the user's git credentials
mk["spanner"] = {"source": {"source": "github",
                            "repo": "spanner-product-dev/spanner-claude-marketplace"},
                 "autoUpdate": True}
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
