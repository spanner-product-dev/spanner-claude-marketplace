# Matrix standards & SQL templates

## matrix_tasks schema (the columns this skill touches)

| Column | Type | Notes |
|---|---|---|
| task_id | text PK | Legacy `Q1.1`/`Q2-new.3` style or stable `YYMMDD-N` |
| title | text | |
| short_name | text | slug for Slack/Notion refs, e.g. `ca-privacy-policy` |
| theme | text | forge / bd / team / marketing / website / delivery / portal / tooling (+ custom) |
| impact, effort | numeric(4,2) | 1.0–3.9; don't change on status updates |
| quadrant | text | Q1/Q2/Q3/Q4 — derived: Q1 i≥2,e<2 · Q2 i≥2,e≥2 · Q3 i<2,e<2 · Q4 i<2,e≥2 |
| status | text | unstarted / next / in_progress / done / deferred / cancelled / unconfirmed |
| urgency | text | null / 'week' / 'now' / 'today' |
| owner | text | may be multi: "Giles / Andy" |
| source / source_url | text | where the task came from + deep link |
| notes | text | soft convention: `Status: … / Next: … / Blocked by: …` |
| last_edited_by | text | 'Claude' for skill writes |
| date_created / date_assigned / date_started / date_completed | timestamptz | set date_started on →in_progress, date_completed on →done |

`matrix_comments`: id UUID PK (auto), task_id FK, author, body, created_at (auto).

## ID scheme

`YYMMDD-N` — creation date for new work; **completion** date for retroactively-logged completed work. N = sequence within that day (check existing IDs first: `select task_id from matrix_tasks where task_id like '260612-%'`).

## Scoring rubric (only when creating new tasks)

Impact: 3 = direct revenue lever (pipeline, deals, client work) · 2 = enables a revenue lever / team multiplier / margin · 1 = internal hygiene.
Effort: 1 = ≤ half-day · 2 = 1–5 days · 3 = > 1 week.

## File numbering

Next file = highest `matrix_0*.sql` in the workspace folder + 1. As of 2026-06-04 the highest is `matrix_011_jun4_completed.sql`.

## Template — status change (e.g. work started / finished)

```sql
-- matrix_0NN_<slug>.sql — <one-line purpose>
-- Safe to re-run: plain UPDATEs, idempotent.
begin;
update matrix_tasks set status='in_progress', date_started=coalesce(date_started, now()),
  last_edited_by='Claude' where task_id='<ID>';
update matrix_tasks set status='done', date_completed='<YYYY-MM-DD>',
  last_edited_by='Claude' where task_id='<ID2>';
commit;
-- Verify: select task_id,status,date_started,date_completed from matrix_tasks
--   where task_id in ('<ID>','<ID2>');
```

## Template — new / completed task entry

```sql
insert into matrix_tasks
    (task_id, title, short_name, theme, impact, effort, quadrant, status, urgency, owner,
     source, source_url, notes, last_edited_by, date_created, date_completed)
values
    ('YYMMDD-N', '<title>', '<slug>', '<theme>', 2.0, 1.0, 'Q1', 'done', null, '<Owner>',
     '<source>', '<url or null>', '<context>', 'Claude', 'YYYY-MM-DD', 'YYYY-MM-DD')
on conflict (task_id) do update set
    title=excluded.title, short_name=excluded.short_name, theme=excluded.theme,
    impact=excluded.impact, effort=excluded.effort, quadrant=excluded.quadrant,
    status=excluded.status, owner=excluded.owner, source=excluded.source,
    source_url=excluded.source_url, notes=excluded.notes,
    last_edited_by=excluded.last_edited_by, date_completed=excluded.date_completed;
```

For active (not completed) tasks: status `'unstarted'`/`'next'`, `date_completed` null, drop that column from the insert.

## Template — meeting-reference comments (post-meeting routine)

```sql
-- NOT idempotent — check before running:
-- select count(*) from matrix_comments where body like '%<Meeting name, date>%';
insert into matrix_comments (task_id, author, body) values
  ('<ID>', 'Claude', 'Discussed: <Meeting>, <Mon D> — <one-line outcome> — https://app.notion.com/p/<page-id>'),
  ('<ID>', 'Claude', 'Created: <Meeting>, <Mon D> — https://app.notion.com/p/<page-id>');
```

Post-meeting routine: read the Notion/Granola page → identify created + discussed tasks → comments for each → new-task inserts → status patches → fill the MATRIX frontmatter block and `Task IDs` property on the Notion page.

## REST API patterns (when network allows)

```bash
SB=https://lyerknxfxesoecmpipip.supabase.co/rest/v1
# read (orient / verify)
curl -s "$SB/matrix_tasks?select=task_id,title,short_name,status,urgency,owner&status=eq.in_progress" \
  -H "apikey: $SB_KEY" -H "Authorization: Bearer $SB_KEY"
# patch
curl -s -X PATCH "$SB/matrix_tasks?task_id=eq.<ID>" -H "apikey: $SB_KEY" \
  -H "Authorization: Bearer $SB_KEY" -H "Content-Type: application/json" \
  -H "Prefer: return=minimal" -d '{"status":"done","date_completed":"<ISO>","last_edited_by":"Claude"}'
# insert (upsert)
curl -s -X POST "$SB/matrix_tasks" -H "apikey: $SB_KEY" -H "Authorization: Bearer $SB_KEY" \
  -H "Content-Type: application/json" -H "Prefer: resolution=merge-duplicates,return=minimal" \
  -d '[{"task_id":"YYMMDD-N", ...}]'
```

`$SB_KEY` = anon key from `matrix-overall.html` (`const SB_KEY`).

## After every sync

Update `TASKS-ACTIVE.md`: move completed rows to "Recently Completed", add new NOW/WEEK items, refresh the date in the header. If the change is strategically significant, reflect it in `plan-overall.md` too.
