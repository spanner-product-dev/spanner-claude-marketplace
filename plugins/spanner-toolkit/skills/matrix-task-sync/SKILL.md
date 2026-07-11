---
name: matrix-task-sync
description: Keeps the SpannerOS prioritization matrix (Supabase) in sync with actual work. Use whenever Mason reports work happening or finished — "mark X done in the matrix", "I finished the privacy policy", "update the matrix", "log this in the matrix", "new task from today's meeting", "set X to in progress", "add what we did today", "matrix sync", or at the end of any session where tracked work changed status. Identifies which matrix tasks the work maps to (via TASKS-ACTIVE.md and task titles/short_names), then either applies the change directly via the Supabase REST API or generates a numbered, idempotent SQL migration file to run in the SQL editor. Also use after meetings to add meeting-reference comments and new tasks per the established standards.
---

# Matrix Task Sync

The prioritization matrix is the single source of truth for Spanner's open and completed work. This skill turns "I did X" into the correct database update — without Mason hand-editing rows.

## Source of truth

| Thing | Value |
|---|---|
| Supabase project | `lyerknxfxesoecmpipip` |
| Tables | `matrix_tasks` (PK `task_id`), `matrix_comments` (FK `task_id`) |
| Live matrix UI | https://spanneros-wip.pages.dev/_Overall_Plan_and_Prioritization/matrix-overall |
| SQL editor | https://supabase.com/dashboard/project/lyerknxfxesoecmpipip/sql/new |
| Workspace folder | `Projects/Overall Planning and Prioritization/` (SQL files, TASKS-ACTIVE.md, plan-overall.md) |
| Anon key | In `matrix-overall.html`, `const SB_KEY = '...'` (public anon key; RLS grants full CRUD) |

## Workflow

1. **Orient.** Read `TASKS-ACTIVE.md` first; if more context is needed, read `plan-overall.md`. These map work descriptions to task IDs and short_names.
2. **Identify the task(s).** Match what Mason describes against task titles, short_names, and IDs. If ambiguous, ask — never guess between two plausible tasks.
3. **Apply the change** — two paths, try in order:
   - **Direct REST** (works when the environment can reach supabase.co — Cowork sandboxes often cannot):
     ```bash
     curl -s -X PATCH "https://lyerknxfxesoecmpipip.supabase.co/rest/v1/matrix_tasks?task_id=eq.<ID>" \
       -H "apikey: $SB_KEY" -H "Authorization: Bearer $SB_KEY" \
       -H "Content-Type: application/json" -H "Prefer: return=representation" \
       -d '{"status":"done","date_completed":"<ISO date>","last_edited_by":"Claude"}'
     ```
   - **SQL migration file** (the default; always works): write `matrix_0NN_<slug>.sql` to the workspace folder, where NN = highest existing `matrix_0*.sql` number + 1. Mason pastes it into the SQL editor. Tell him explicitly that the file needs to be run.
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
