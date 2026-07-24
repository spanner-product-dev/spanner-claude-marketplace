---
name: matrix-task-sync
description: Keeps the SpannerOS prioritization matrix (Supabase) in sync with actual work. Use whenever Mason reports work happening or finished — "mark X done in the matrix", "I finished the privacy policy", "update the matrix", "log this in the matrix", "new task from today's meeting", "set X to in progress", "add what we did today", "matrix sync", or at the end of any session where tracked work changed status. Identifies which matrix tasks the work maps to (via TASKS-ACTIVE.md and task titles/short_names), then applies the change as a numbered, idempotent SQL migration pushed with the Supabase CLI (`supabase db push`) — direct Supabase REST is only a fallback when reachable, and pasting into the SQL editor is deprecated. Also use after meetings to add meeting-reference comments and new tasks per the established standards.
---

# Matrix Task Sync

The prioritization matrix is the single source of truth for Spanner's open and completed work. This skill turns "I did X" into the correct database update — without Mason hand-editing rows.

## Source of truth

| Thing | Value |
|---|---|
| Supabase project | `lyerknxfxesoecmpipip` |
| Tables | `matrix_tasks` (PK `task_id`), `matrix_comments` (FK `task_id`) |
| Live matrix UI | https://spanneros-wip.pages.dev/_Overall_Plan_and_Prioritization/matrix-overall |
| SQL editor | https://supabase.com/dashboard/project/lyerknxfxesoecmpipip/sql/new (ad-hoc/verify only — not the migration path) |
| CLI migration project | `~/Developer/spanner-matrix-db` (outside Google Drive); `supabase db push` applies migrations |
| Migration history | `supabase_migrations.schema_migrations` (version, name, `statements` = SQL body — searchable). In-dashboard view = the saved "List CLI Queries" snippet |
| Workspace folder | `Projects/Overall Planning and Prioritization/` (SQL files archive, TASKS-ACTIVE.md, plan-overall.md) |
| Anon key | In `matrix-overall.html`, `const SB_KEY = '...'` (public anon key; RLS grants full CRUD) |

## Workflow

1. **Orient.** Read `TASKS-ACTIVE.md` first; if more context is needed, read `plan-overall.md`. These map work descriptions to task IDs and short_names.
2. **Identify the task(s).** Match what Mason describes against task titles, short_names, and IDs. If ambiguous, ask — never guess between two plausible tasks.
3. **Apply the change** — the standard path is a CLI migration (decided 2026-07-22; supersedes SQL-editor paste):
   - **CLI migration file (default).** Write `matrix_0NN_<slug>.sql` to the workspace folder (NN = highest existing `matrix_0*.sql` + 1; check for parallel-session collisions — a number may exist that isn't in the folder). Idempotent, begin/commit-wrapped, verification query in a footer comment. Mason applies it from `~/Developer/spanner-matrix-db`:
     ```bash
     cd ~/Developer/spanner-matrix-db
     supabase migration new matrix_0NN_<slug>
     MIG=$(ls -t supabase/migrations/*matrix_0NN_<slug>.sql | head -1)
     cp "<workspace-folder>/matrix_0NN_<slug>.sql" "$MIG"
     supabase db push
     ```
     It lands in `supabase_migrations.schema_migrations` (searchable via the "List CLI Queries" snippet). Give Mason comment-free command blocks (zsh chokes on `#`-comment lines with parens: `parse error near ')'`).
     - **First-time / history gotchas:** on a DB built by SQL-editor migrations, push can error "Remote migration versions not found in local" — fix with `supabase migration repair --status reverted <version>` (edits the bookkeeping table only, NO schema change), then push. The Docker-daemon warning on `db push` is harmless (Docker only needed for local dev, not hosted push).
   - **Direct REST (fallback only, when supabase.co is reachable — Cowork sandboxes usually can't):**
     ```bash
     curl -s -X PATCH "https://lyerknxfxesoecmpipip.supabase.co/rest/v1/matrix_tasks?task_id=eq.<ID>" \
       -H "apikey: $SB_KEY" -H "Authorization: Bearer $SB_KEY" \
       -H "Content-Type: application/json" -H "Prefer: return=representation" \
       -d '{"status":"done","date_completed":"<ISO date>","last_edited_by":"Claude"}'
     ```
4. **Mirror the change in `TASKS-ACTIVE.md`** (move rows between sections, add completions) and, for significant items, in `plan-overall.md`.
5. **Report** which task IDs changed and how.

See `references/standards.md` for the schema, ID rules, scoring rubric, and copy-paste SQL templates. Follow them exactly — consistency is the whole point.

## Hard rules

- New task IDs are `YYMMDD-N` (date + daily sequence). Never invent `Q1.x`-style IDs — those are legacy.
- Completed tasks: `status='done'`, `date_completed` set, `owner` = who did the work, ID date = **completion** date.
- Task INSERTs/UPDATEs must be idempotent (`ON CONFLICT (task_id) DO UPDATE`). Comment INSERTs are **not** idempotent — never re-run a comment block; include a pre-check SELECT in the file.
- `last_edited_by = 'Claude'` on anything this skill writes.
- Status values: `unstarted / next / in_progress / done / deferred / cancelled / unconfirmed`. Urgency: `null / 'week' / 'now' / 'today'`.
- Don't change impact/effort scores when marking status — scoring is a human decision unless Mason asks.
- One SQL file per session/batch, not per task. Begin/commit wrapped, verification query in a footer comment.
