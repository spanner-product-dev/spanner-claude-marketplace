---
name: spanner-weekly-digest
description: >
  Generates a structured ops brief for Spanner PD by pulling active project status from Notion,
  team activity from Slack, and surfacing anything that needs Mason's attention. Use whenever Mason
  wants a weekly status overview, Monday morning briefing, project health check, or a catch-up on
  what's happening. Triggers on: weekly digest, Monday brief, what's on my plate this week, project
  status sweep, what's happening at Spanner, catch me up, what do I need to know, ops brief, give
  me the weekly, or any request for a summary of current Spanner project activity. Always invoke
  this skill for these requests — it knows which Notion database to query, how to scan Slack for
  relevant signals, and how to format the output as a scannable 2-minute brief.
---

# Spanner Weekly Digest

## What this produces

A brief, scannable ops summary covering:
1. Active project health (from Notion project tracker)
2. Slack highlights — blockers, flags, open threads that need attention
3. Surfaced action items based on the above

Runs in 2–3 minutes. No Harvest data yet (that comes when SpannerOS Phase 3 ships).

---

## Step 1: Pull active projects from Notion

Query the Spanner Project Tracker. The collection ID is `efb9ea40-a2ae-4130-8d34-4cd0a39c8101`.

Use `notion-query-database-view` or `notion-fetch` with this collection ID. Filter for active/live projects only — skip anything completed, on hold, or in backlog.

For each active project, capture whatever is available:
- Project name
- Client name
- Project status / health indicator
- PM or TPL assigned
- Any flags, alerts, or notes visible in the tracker

**Important:** The Program Launch Checklists Notion page (`4eee597dc8c642078d44dbd5fe83d03a`) always times out via API — skip it entirely, do not retry. If the project tracker query itself times out, note it in the brief and continue — don't block the rest of the digest waiting for Notion.

---

## Step 2: Scan Slack for relevant activity

Search the past 5–7 days. Goal is signal, not volume — pull 3–5 notable items, not a full transcript.

Look for:
- Messages in any channel mentioning active project names from Step 1
- Messages containing words like "blocked", "blocker", "delayed", "overdue", "urgent", "help needed", "waiting on"
- Any direct mentions of Mason (check @mason, @mason_curry, or similar)
- Anything in studio channels (#spanneros, #studio, #general, #projects) that reads like a status update or decision

If Slack search returns too many results, focus on the ones most likely to need follow-up: questions without responses, flagged items, anything from the past 48 hours.

---

## Step 3: Format the brief

Use this exact structure. Keep it tight — this is a 2-minute Monday morning read, not a report.

```
# Spanner Weekly Brief — Week of [DATE]
_Generated [TODAY'S DATE]_

---

## Active Projects ([N] active)

| Project | Client | PM/TPL | Status | Notes |
|---------|--------|--------|--------|-------|
| ...     | ...    | ...    | ...    | ...   |

---

## Slack Highlights

- [2–5 bullet points — notable mentions, open threads, or flags from the past week]
- If nothing notable: "Nothing flagged this week."

---

## Action Items

1. [Things that appear to need Mason's attention, pulled from signals above]
2. [Blocked items, unanswered questions, upcoming decisions]
- If nothing: "No immediate action items surfaced."

---

## Data gaps

- [Note anything unavailable — e.g., "Notion project tracker returned no results", "No Harvest data until Phase 3"]
```

---

## Tone and style

Plain, factual, direct. This is a quick scan, not a memo. Skip filler phrases like "it appears that" or "based on the available data." If a section has nothing to report, say "Nothing flagged" in one line.

Don't editorialize — report what's in the data. If something looks concerning (e.g., a project has been in the same status for three weeks), surface it as a fact, not an alarm.

---

## Known limits

- No Harvest time data until SpannerOS Phase 3 (API integration not yet built)
- Notion Program Launch Checklists always timeout — always skip
- Slack search may not surface private channel content depending on connector scope
- New Notion multi-select values (like new Client names) may not appear if added manually after the last API sync
