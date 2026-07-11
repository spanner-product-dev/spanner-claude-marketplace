#!/usr/bin/env bash
# Spanner security pre-commit/push gate (Claude Code PreToolUse hook).
#
# Fires before every Bash tool call; acts only on `git commit` / `git push`.
# Hard-BLOCKS (permissionDecision: deny) when the change would introduce an
# unambiguous secret: a secret/key file staged, a private-key block, an AWS
# access key, or a Supabase service_role key value. High precision by design —
# the deterministic gate catches the catastrophic; the LLM skill catches the
# nuanced. Fails OPEN on infra errors so it never wedges normal work.
set -uo pipefail

input="$(cat)"

# Bash command about to run (robust JSON parse; fail open if unparseable).
cmd="$(printf '%s' "$input" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)"
[ -z "$cmd" ] && exit 0

# Only gate git commit / git push.
echo "$cmd" | grep -Eq 'git[[:space:]]+(commit|push)' || exit 0

# Must be inside a git work tree.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

label="commit"
is_push=false
if echo "$cmd" | grep -Eq 'git[[:space:]]+push'; then label="push"; is_push=true; fi

# What is about to land: file names + added content.
if $is_push; then
  names="$(git log --name-only --pretty=format: --branches --not --remotes 2>/dev/null | sort -u | sed '/^$/d')"
  content="$(git log -p --no-color --branches --not --remotes 2>/dev/null)"
else
  names="$(git diff --cached --name-only 2>/dev/null)"
  content="$(git diff --cached --no-color 2>/dev/null)"
fi
[ -z "$names$content" ] && exit 0

# Only added lines matter for content checks.
added="$(printf '%s\n' "$content" | grep -E '^\+' 2>/dev/null || true)"

reasons=""
add_reason() { reasons="${reasons}"$'\n'"  - $1"; }

# 1) Secret / key files being committed (skip .example and .md docs).
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in *.example|*.md) continue;; esac
  if printf '%s' "$f" | grep -Eiq '(^|/)\.env($|\.)|\.pem$|\.p12$|(^|/)id_rsa$|\.key$|(^|/)credentials(\.json)?$'; then
    add_reason "secret/key file staged: $f  — never commit this; add it to .gitignore"
  fi
done <<< "$names"

# 2) Private key block.
printf '%s' "$added" | grep -Eq -- '-----BEGIN [A-Z ]*PRIVATE KEY-----' && \
  add_reason "a private-key block is in the change"

# 3) AWS access key id.
printf '%s' "$added" | grep -Eq 'AKIA[0-9A-Z]{16}' && \
  add_reason "an AWS access key id (AKIA...) is in the change"

# 4) Supabase service_role key value.
printf '%s' "$added" | grep -Eiq 'SUPABASE_SERVICE_ROLE_KEY[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9._-]{20,}' && \
  add_reason "SUPABASE_SERVICE_ROLE_KEY has a value in the change — service_role must live only in a server secret store, never in the repo"

if [ -n "$reasons" ]; then
  reason="Spanner security gate blocked this ${label}. Fix before proceeding:${reasons}

Per the Spanner security standard: no secrets in the repo — env vars / platform secret store only. If a secret was already committed, revoke and rotate it in the issuing platform first (deleting the file does not clear git history)."
  python3 - "$reason" <<'PY'
import json,sys
print(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":sys.argv[1]}}))
PY
  exit 0
fi

exit 0
