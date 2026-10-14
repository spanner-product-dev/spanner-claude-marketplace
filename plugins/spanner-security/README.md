# spanner-security (Claude Code plugin)

Ships the **spanner-security-standard** skill: Spanner PD's secure-by-default engineering standard as an always-on skill for Claude Code.

The skill loads automatically whenever Claude builds or reviews anything touching code, data, auth, or deployment — starting a repo, writing a Supabase migration, adding auth, setting up RLS, handling secrets, configuring Cloudflare, or wiring a deploy. It enforces the five rules (no secrets in repos; RLS deny-by-default from the first migration; server-side authorization; `service_role` stays server-side; Layers 1 & 2 always on) and runs the New-Project Checklist before feature code.

## Contents
- `skills/spanner-security-standard/SKILL.md` — the standard, summarized and made actionable
- `skills/spanner-security-standard/references/full-standard.md` — the full GitHub / Supabase / Cloudflare rules + three-layer compliance framework

## Hooks
- `hooks/check-secrets.sh` (PreToolUse, Bash) — scans every Bash command for secrets before it runs.
- `hooks/history-check.py` (Stop) — **session-log gate.** If a session's last edit, `git commit`/`push` or `gh pr create`/`merge` came after its last write to `history/session-history.md` or `history/YYYY-MM.md`, it blocks the end of the turn once and tells Claude to log the session (create `history/` if the project has none). Ignores edits under `~/.claude`, `/tmp` and scratchpads; `stop_hook_active` prevents loops. It lives here only because every teammate already has this plugin pinned on; it is not a security control. Needs `python3`. The rule it enforces is in the org instructions ("Log every session in `history/`").

## Keeping it current
The canonical source is `SpannerOS/Security Framework/spanner-security-standard.md`. When that changes, update the skill here, bump the version in `.claude-plugin/plugin.json` and the marketplace entry, and re-publish.
