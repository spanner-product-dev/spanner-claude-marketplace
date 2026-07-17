---
name: spanner-meeting-notes
description: Generates Spanner meeting notes from a Granola, Zoom, or Otter transcript and publishes them to the right Notion database, with Slack routing per meeting type. When the author captured screenshots during the call — portal-hotkey captures or their own macOS screenshots — it enriches the notes by matching each screenshot to the moment in the transcript, copying and renaming local screenshots into the portal (or attaching them to Notion) on the way. Use whenever anyone at Spanner asks for meeting notes, a summary, or a write-up — "write up the [meeting]", "summarize the standup/sync/TPL", "publish notes to Notion", "meeting notes with screenshots", "add screenshots to my notes". Screenshots are optional enrichment, not required. When in doubt, use this skill — it knows the source connectors, folder paths, URL patterns, timestamp conventions, and Notion database IDs plain summarization would have to rediscover.
---

# Spanner Meeting Notes

Generate meeting notes from a Granola, Zoom, or Otter transcript, publish them to
the correct Notion database, and post to the right Slack channel when asked.

**Screenshots are enrichment, not the point.** There are two possible sources,
and either (or neither) may exist for a given meeting:

- **Portal-hotkey captures** — some teammates run a hotkey that captures a window
  mid-meeting and saves it straight to the portal repo, already web-addressable.
- **The author's own macOS screenshots** — ordinary ⌘⇧4/⌘⇧5 captures taken during
  the call, sitting in the user's screenshot folder. These are *not* web
  addressable, so the skill finds the in-window ones, copies them into the portal
  (renamed to the portal convention) or attaches them to Notion, then embeds them.

When captures exist for the meeting window, each one is matched to the exact
moment in the transcript — so the notes embed the image *and* describe what the
team was looking at while discussing it. When none exist (the common case for
most people), write normal notes and skip the enrichment steps silently — don't
treat the absence as an error.

This skill is org-wide. It resolves **the current user** (the meeting author)
from context — use their identity for attribution, their calendar for
disambiguation, and their per-user catch-all database as the routing default.
Never hardcode a specific person.

## Transcript sources (any one is enough)

Pull whichever the author used; prefer the richest available, and combine when
more than one exists:

- **Granola** — `list_meetings` → `get_meetings`. Gives date/start, attendees, AI
  summary, and in `private_notes` often the full timestamped transcript.
  `get_meetings` responses can overflow to a results file — read that file
  completely (in chunks); the transcripts at the end are where the timestamps
  live.
- **Zoom** — `search_zoom` (`entity_type: zoom_doc`, `doc_view: notes`) +
  `get_file_content` for AI notes; recordings/transcripts via the Zoom recording
  tools. Zoom AI notes frequently carry decisions/action items the Granola
  summary missed — pull both when writing full notes.
- **Otter** — use the Otter transcript/notes export when that's what the author
  has (pasted in chat, dropped in Drive, or via an Otter connector if one is
  configured). Otter gives speaker-labeled lines and a summary the same way.
- **Local Transcripts folder** — Zoom/Otter exports are often dropped as `.txt`
  files in the author's Transcripts folder (Mason: the connected **Transcripts**
  Google Drive folder). This is frequently the *only* source, since Granola/Zoom
  connectors may return nothing for a given meeting. Fresh exports often land with
  a generic name (`transcript.txt`, `transcript1.txt`) or a raw export name
  (`SpannerOS Sync 2026-07-09 10_34(GMT-7_00).txt`) — identify the meeting from
  the first timestamp + speakers, then **rename it to the folder convention** (see
  the infra table and step 1).

**Timestamp normalization (important for screenshot matching).** Granola/Zoom
lines carry Pacific **wall-clock** times (`**Giles Lowe** 11:02:44`). Otter
exports often use **elapsed** time from the start of the recording (`0:12:44`,
i.e. mm:ss or h:mm:ss). Before correlating with screenshots, convert every
transcript timestamp to Pacific wall-clock — for elapsed-time transcripts, add
the offset to the meeting's scheduled/actual start time. If you can't establish a
reliable start time, say so and fall back to notes without screenshot
correlation.

If no transcript source is reachable, tell the user which connectors are
missing and ask them to paste an export rather than guessing at content.

## Key infrastructure facts

| Thing | Value |
|---|---|
| Portal screenshots folder (host) | `~/Developer/spanner-internal-website/public/screenshots/YYYY-MM/` |
| Portal filename convention | `YYYYMMDD-HHMMSS-label.png` — **Pacific time** (e.g. `20260605-153541-meeting.png` = 3:35:41 PM PT) |
| Live URL pattern | `https://spanneros-wip.pages.dev/screenshots/YYYY-MM/<filename>` |
| Portal SSO | The portal is behind Cloudflare Access — image embeds in Notion may not render for Notion's proxy even though links work for the team in a browser |
| Local macOS screenshot folder (per-user) | Resolve in order: (1) `defaults read com.apple.screencapture location`; (2) the user's configured/known folder; (3) `~/Desktop` (macOS default). The user can also just name it or paste files. Known configs — Mason: `~/Documents/Screenshots`. |
| macOS screenshot filename | `Screenshot YYYY-MM-DD at H.MM.SS AM/PM.png` — **Pacific local wall-clock**, 12-hour, unpadded hour, dot separators (e.g. `Screenshot 2026-07-13 at 11.36.33 AM.png` = 11:36:33 AM PT). If a name is unparseable, fall back to the file's modification time. |
| Local transcripts folder (per-user) | Mason: the connected **Transcripts** Google Drive folder. Fresh Zoom/Otter exports may arrive as `transcript.txt` / `transcript1.txt` or a raw export name. |
| Transcript filename convention | `YYMMDD-HHMM_Meeting_Name.txt` — 2-digit year, 24-hour **Pacific** start time, underscores in the name (e.g. `260717-1300_TPL_Sync.txt`, `260713-1030_SpannerOS_Standup.txt`). Rename any generically-named export to this before finishing. |

If the repo folder isn't mounted, request it via `request_cowork_directory` with
path `~/Developer/spanner-internal-website`. If the user doesn't have that repo
or hasn't set up capture, **skip screenshots entirely and continue** — this is
expected, not a failure. Old screenshots (pre Jun 5 2026, names like
`2026...-22xxxx-shot.png`) used UTC; everything after uses Pacific.

## Routing — which Notion database and Slack channel per meeting

Pick the destination from this table before publishing. Post the notes link to
the Slack channel only when the user asks (or has asked for that meeting type
before in the same session). "Author's catch-all" = the current user's per-user
meeting-notes database (see resolution below).

The Google Calendar **"SpannerOS Standup"** (recurring ~10:30 AM PT bi-daily;
Mason, Torence, Arne, Marielle, Giles) is a **BD / ops check-in**, not an
app-dev standup — despite the name it covers pipeline (Luxshare etc.),
website/SEO, and Bullhorn/staffing. When the meeting reference is ambiguous,
**confirm against the current user's calendar** (match by time), then route via
the table.

| Meeting | Notion database | Type property | Slack channel |
|---|---|---|---|
| TPL Sync | Spanner Meetings - General (`fdf3b3e6-6e8f-4088-a2bf-378002ba30ab`) | TPL Weekly | `#technical-program-leads-tpl` (`C02CA1WLW13`) |
| Weekly Team Meeting | Spanner Meetings - General | Team weekly | `#technical-program-leads-tpl` (`C02CA1WLW13`) |
| SpannerOS Standup (10:30 bi-daily BD/ops) | SpannerOS \| Meetings and Project Notes (Internal) (`35f222a7-d409-812c-839e-f349e0712393`, data source `collection://35f222a7-d409-8101-8caf-000bbb329394`) | Standup | `#spanner-os` (`C0B3Z6JLSLB`) |
| Tin meetings / exec reviews (K5 etc.) | Author's catch-all | Exec Review | `#exec_reviews` (`C06ED2SFHFA`) when asked |
| VitalBio / Viking | VitalBio \| Viking \| Meetings and Project Notes (`276222a7-d409-81b4-a675-d226afd0b872`) | — | `#vitalbio` (`C09GYJDPKB3`) |
| Gigamon / Scout | Author's catch-all | — | `#gigamon` (`C0AMVT06GMU`) |
| Neuring HW Feasibility | Author's catch-all | — | `#neuring-hw-feasibility` (`C0B65CD1727`) |
| CRL / PTS Next Gen | CRL \| PTS Next Gen \| Meetings and Project Notes (`211222a7-d409-8114-af0c-dcb34f5d915d`) | — | TBD |
| Other client/project meetings | That project's "Client \| Project \| Meetings and Project Notes (Internal)" DB **only if it exists with a real (non-template) title**; otherwise the author's catch-all | — | The project's Spanner-internal channel (e.g. `#blend-health`, `#wispr`, `#leafi`, `#viviscout`) |
| 1:1s | Author's catch-all | Ad Hoc | none |
| Ad-hoc / anything not listed above | Author's catch-all (default unless the user says otherwise) | Ad Hoc | none unless asked |

### Resolving the author's catch-all (per-user)

Each teammate has (or gets) their own catch-all meeting-notes database, named by
convention **"Meeting Notes db - {FirstName}"**. To resolve it:

1. Determine the current user's first name from context (their email / profile).
2. `notion-search` for `Meeting Notes db - {FirstName}`. If a database with that
   exact-style title exists, use it — fetch it first to get its `collection://`
   data source ID before creating pages.
3. If none exists, ask the user whether to create one (title
   `Meeting Notes db - {FirstName}`, properties matching the standard below) or
   to fall back to **Spanner Meetings - General**
   (`collection://5e5df0db-dc4a-4447-b277-56b7925499d4`). Don't silently invent a
   database.

Standard catch-all properties: `Name` (title), `date:Meeting Date:start`, `Type`
(select: Standup, Weekly Sync, Design Systems, Ad Hoc, Post-mortem, Sprint
Planning, Kickoff, Troubleshooting, TPL Sync, Exec Review, Design Review),
`Entry Type` (set to "Meeting"), `Client` (select — add the client name when it
matches an option).

**Spanner Meetings - General** (shared): data source
`collection://5e5df0db-dc4a-4447-b277-56b7925499d4`. Properties: `Name` (title),
`date:Meeting Date:start`, `Type` (select: Standup, Brainstorm, Team weekly,
Training, TPL Weekly, Lunch n Learn).

**Private channels** don't appear in `slack_search_channels`. Known private
channels: `#spanner-os` (`C0B3Z6JLSLB`), `#os-website`,
`#technical-program-leads-tpl` (`C02CA1WLW13`), `#spanner-team`, `#finance-tpl`,
`#exec_reviews` (`C06ED2SFHFA`), `#leadership`, `#code-spark`, `#ai-small-group`,
`#ext-viviscout-spanner`. To resolve a missing private-channel ID, run
`slack_search_public_and_private` with query `in:#<channel-name>` — the results
include the channel ID.

The default for anything unrouted is the **author's catch-all** — not Spanner
Meetings - General. Many per-project DBs are still unfilled templates titled
"[Client] | [Project] | Meetings and Project Notes (Internal)" — never publish
into a template; use the catch-all instead. Fetch a database first to get its
`collection://` data source ID before creating pages, and update this table when
a new destination is confirmed.

## People glossary (for correct attribution)

- **Larry Copponi** — VP Staffing Solutions; owns recruiting/staffing + Bullhorn (staffing ATS).
- **Andy** — external Webflow developer building the new marketing site.
- **Damien Golbin** — program lead/engineer; "an extension" usually = a client SOW/contract extension.
- **"Camp Loma"** (often mis-transcribed "Comp Loma") — Spanner hardware-founders event, Aug 22–23.
- Transcripts frequently render **Arne Lang-Ree** as **"Anna."**

## Workflow

### 1. Resolve the meeting and its time window

Find the meeting in the available source (Granola / Zoom / Otter) and get its
date, start time, attendees, and summary. The meeting window = scheduled start
until the last transcript timestamp (pad by ±5 minutes; people screenshot a beat
before or after the moment).

**Attendees — derive from the transcript, not the invite list.** Granola lists
every *invitee* as an attendee even when they never joined, so the invite list
overstates who was there. The reliable signal is who actually has spoken lines
in the transcript. So: list as present the people with transcript utterances,
and for invitees who never spoke, note them separately as invited but unconfirmed
(they may have been silent, absent, or dialed in without talking — don't assert
they were absent). Example: "Present (spoke): Mason, Torence, Giles, Niall.
Invited, didn't speak (unconfirmed): Jorge, Alyssa." If a Slack message in the
channel shows someone explicitly bowing out ("I'll skip today"), you can upgrade
that to "absent."

**Rename the raw transcript file.** If the transcript came from a local
Transcripts folder with a generic or raw export name (`transcript.txt`,
`transcript1.txt`, `SpannerOS Sync 2026-07-09 10_34(GMT-7_00).txt`), rename it to
the convention `YYMMDD-HHMM_Meeting_Name.txt` using the meeting's Pacific start
time derived from the first transcript timestamp (e.g. `260717-1300_TPL_Sync.txt`).
Do this even when there are no screenshots — it keeps the folder consistent and is
part of finishing the job. Match the `Meeting_Name` to how sibling files in the
folder are named.

### 2. Find in-window screenshots (enrichment — skip if none)

**Mount both folders first.** The portal repo
(`~/Developer/spanner-internal-website`) and the author's local screenshot folder
(e.g. `~/Documents/Screenshots`) may each need mounting via
`request_cowork_directory` before you can open images: `Glob` can *list* files in
an unmounted path, but `Read` cannot open them until the folder is connected.
Request both, then list and read.


Gather from both possible sources; use whichever exist. In all cases, "in window"
= the meeting window from step 1, padded ±5 min. If the user pasted a specific
URL/file or mentioned "the screenshot I just took," include it regardless.

**a) Portal-hotkey captures.** List `public/screenshots/<YYYY-MM>/` and parse
each filename's `YYYYMMDD-HHMMSS` timestamp as Pacific wall-clock. Keep files
inside the window. Already web-addressable — no import needed.

**b) The author's own macOS screenshots.** Resolve the user's local screenshot
folder (detection order in the infra table; ask or accept a pasted path if
unsure). List it and parse each `Screenshot YYYY-MM-DD at H.MM.SS AM/PM.png`
name as Pacific local wall-clock (fall back to file mtime for odd names). Keep
files inside the window.

If neither source yields anything in-window — or the folders/repo aren't
available — skip the remaining screenshot steps and go straight to composing
notes. Never pad with out-of-window images.

### 2b. Import local screenshots (copy → rename → publish)

macOS screenshots aren't web-addressable, so before they can be embedded, import
each in-window local screenshot found in step 2(b):

1. **Copy** it into `~/Developer/spanner-internal-website/public/screenshots/<YYYY-MM>/`
   (create the month folder if missing).
2. **Rename** to the portal convention `YYYYMMDD-HHMMSS-<meeting-slug>.png` using
   the parsed capture time — e.g. `Screenshot 2026-07-13 at 11.36.33 AM.png` for
   the SpannerOS standup → `20260713-113633-spanneros-standup.png`. Never
   overwrite: if the target name already exists, append `-2`, `-3`, … Keep a map
   of {original file → new portal filename} so captions and correlation use the
   parsed time.
3. **Publish.** Once the portal deploys (the repo's normal auto-deploy/watcher, or
   the `spanner-internal-deploy` skill), each imported shot is live at
   `https://spanneros-wip.pages.dev/screenshots/<YYYY-MM>/<newname>` — embed by
   that URL exactly like the hotkey captures (same SSO render caveat).
4. **Fail gracefully.** If the portal repo isn't mounted, or the user would rather
   not deploy personal screenshots to the portal, **attach the image directly to
   the Notion page instead** via `notion-create-attachment` — that renders in
   Notion without the SSO limitation. State which path you took, and default to
   the Notion-attachment path if the portal repo is unavailable rather than
   dropping the image.

### 3. Look at every screenshot

Read each image with the Read tool (the local original is fine — read before or
after the copy). Knowing what's actually pictured is the point — a resourcing
dashboard, a CAD view, a Slack thread — and it often corrects ambiguous
transcript references ("this number here"). This is also the filter: a personal
macOS screenshot folder may hold in-window shots that have nothing to do with the
meeting — if a shot's content clearly doesn't match the discussion, drop it (and
don't import it in 2b).

### 4. Correlate with the transcript

For each screenshot, find the utterances spanning roughly 60s before to 120s
after its timestamp — that's the discussion it illustrates. (Normalize
transcript timestamps to Pacific wall-clock first — see Transcript sources.) Use
the image + surrounding dialogue together: the notes should say what was on
screen *and* what was decided about it.

### 5. Compose the notes

Follow the established structure (plain headings, tight bullets, tables for
action items):

```
<one-line context: meeting, date/time PT, sources, attendees>
# Key Outcomes
# Decisions
# <topic sections as needed>
## During this discussion the team reviewed:  ← screenshot goes here (if any)
# Action Items (see 4-column table format below)
# Sources
```

When screenshots exist, place each inside the topic section it belongs to, with
a caption line stating the capture time and what it shows, e.g.:

```
![Next Week resourcing dashboard](https://spanneros-wip.pages.dev/screenshots/2026-06/20260605-141312-meeting.png)
*2:13 PM — Forecast sheet "Next Week" tab: 23 hrs available; Damien 13, Mason 10*
```

**Action items — 4-column Notion table + carry-over.** Render action items as a
Notion `<table>` with a `<colgroup>` so widths stick:

- Columns, in order: **Owner | Status | Action | Notes**
- Widths: Owner `90`, Status `110` (narrow); Action `380`, Notes `380` (wide)
- For the **current** meeting's new items, leave **Status** and **Notes** blank.
- Add a **"Previous Action Items — Carry-over from [date] standup"** table
  *above* the current one: pull the prior meeting's action list and fill
  Status/Notes with what's known now (statuses: In progress / Done / Not
  started / Ongoing / Unknown), each with a source note.

```
<table header-row="true">
<colgroup>
<col width="90"><col width="110"><col width="380"><col width="380">
</colgroup>
<tr><td>Owner</td><td>Status</td><td>Action</td><td>Notes</td></tr>
...
</table>
```

Note: Notion's API sets column widths (above) but not exact pixels — final
tuning is a UI drag.

### 6. Resolve status & unknown context from other sources

When filling action-item **Status**/**Notes** or answering open questions,
don't stop at the transcript. Cross-reference, in this order, before leaving
anything "Unknown":

1. **Slack** — `#spanner-os` first (the daily standup summaries there are gold),
   then the relevant project channel (`#vitalbio`, `#gigamon`, `#exec_reviews`,
   `#spanner-team`, etc.).
2. **Gmail** — search the person/topic (e.g. "8-Week AI & Staffing Plan",
   "Luxshare").
3. **The matrix** (Supabase) and **prior meeting-notes pages** in the same DB.

Label each resolved item with its source (e.g. "Slack #spanner-os, Jul 6–10").
Only leave a question in "Need Your Input" after these sources come up empty.
Skip any source whose connector isn't authorized rather than failing.

**Always include clickable links to the information sources** in the notes — not
just source names. Link the Slack message permalink, Gmail thread, Notion page,
or portal URL for every status/context item you resolve. Put an inline
`[label](url)` on each resolved 🤖 answer, and collect them under the
**Sources** section split into "Meeting" (transcript, calendar) and "Consulted
for status / context" (the research links). (Reminder: links are fine; never
paste raw `collection://` URIs or internal file paths.)

### 7. Publish to Notion

Create (or update) the page in the database chosen from the routing table.
Set `Name`, `Meeting Date`, and `Type` where the schema has them. Include a
Sources section linking the transcript source (Granola/Zoom/Otter), Slack
channel, and any live dashboards shown in screenshots.

If screenshots were embedded, note the SSO caveat: tell the user the embeds may
render only for logged-in viewers, and offer a link-style fallback if they
appear broken. Never put raw collection:// URIs or internal file paths in the
page.

### 8. Append Claude AI answers + open questions (always)

After publishing, append two sections to the bottom of the page (after Sources):

- **"Open Questions — Resolved (Claude AI)":** answer every unresolved
  question and open decision from the meeting that you reasonably can. Put each
  answer in its own Notion `<callout icon="🤖">` block, and label the text
  explicitly, e.g. `**Claude AI answer — <topic>.**`. Add a 🤖 "Claude AI note"
  callout for any blockers that had a quick, recordable fix.
- **"Open Questions — Need Your Input (for Claude)":** the questions you could
  NOT resolve without more detail, in a single `<callout icon="❓">` block.
  State the easiest way for the team to answer: reply in the meeting's Slack
  channel thread or comment on the Notion page, and the author relays it back to
  Claude.

Be honest about the split — answer what you genuinely can (technical best
practices, tooling fixes, architecture trade-offs) and ask about what needs
team-specific detail; don't fabricate answers. Distinguish Claude's additions
from the team's notes via the "Claude AI" label and the 🤖 / ❓ icons.

**Callout gotcha (formatting).** A `<callout icon="…">` must contain a **single
paragraph** (tab-indented). Do **not** nest a numbered list or multiple blocks
inside one callout — the tags render as escaped literal text. Put the callout
header in its own callout, then place any numbered list as normal blocks after
it. Basic verified syntax: `<callout icon="🤖">` … content … `</callout>`.
Place these two sections after the Sources section.

### 9. Optional follow-ups (only when asked)

- Post the notes link to the relevant Slack channel (Slack can't render the
  SSO-gated images inline — don't try).
- The portal capture hotkey is `screenshot-to-portal.sh` in the
  `spanner-internal-website` repo root (`--window` flag = mid-meeting one-click
  window capture) for any teammate who wants to set up capture or asks how it
  works.

## Edge cases

- **No screenshots in window (or author doesn't capture):** the normal case —
  write standard notes and don't mention missing images or pad with out-of-window
  ones.
- **Missing connector/source:** name the missing connector, use what's available,
  and ask the user to paste an export if no transcript source is reachable.
- **Screenshot of the chat/Claude itself:** usually a workflow test; ask before
  embedding it in client- or team-facing notes.
- **Ambiguous meeting reference:** if two meetings share the day (standup + sync),
  match by time of the screenshots or the current user's calendar, then confirm
  with the user only if still ambiguous.
- **Same screenshot relevant to two topics:** embed once at first mention,
  reference by caption later.
