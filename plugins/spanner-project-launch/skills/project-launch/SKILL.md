---
name: project-launch
description: >
  Automate the Spanner BD-to-PD Launch Checklist for new projects. Use this skill whenever someone says
  "launch a new project", "new project setup", "BD to PD checklist", "project kickoff", "set up a new program",
  "start a new project", "program launch", "launch checklist", "new client project", "kickoff checklist",
  or any variation of starting the BD-to-PD transition process. Also use when someone asks to
  "automate project setup", "run the launch checklist", or references the BD-PD launch process.
  This skill creates Notion pages, Project Tracker entries, Google Drive folders and templates,
  the __SUMMARY forecast row, the Harvest project (via the planner's Provision script) and draft
  deposit invoice, Slack channels and the #spanner-team win post, Google Calendar
  meetings, and notification email drafts — then
  provides a punch list for the remaining manual steps.
---

# Spanner BD-to-PD Project Launch Automation

This skill automates the BD-to-PD Launch Checklist that Spanner runs for every new project. It handles
setup across Notion, Google Drive, Harvest, Slack, Google Calendar, and Gmail, then gives clear instructions
for the steps that still need a human.

## Before You Start (read once per session)

**Connectors needed:** Notion, Google Drive, Slack, Google Calendar, Gmail, Harvest (MCP), plus a browser tool
(Claude's built-in browser pane, or Claude in Chrome) for the Google Sheets / Apps Script / Drive
website steps. If any is missing, say which steps will fall back to the punch list and continue.

**The user must be signed in to Google in that browser.** If Google shows "Verify it's you", the
user signs in — never type credentials. The Apps Script steps also need a one-time script
authorization per person (see Browser Automation Notes).

**Permission prompts:** several steps write to company-wide files (the __SUMMARY forecast, the
case-studies sheet, the rate tracker, DATA STACK, #spanner-team). The session may ask the user to
approve those writes — that is expected. If a write is refused, stop that step, say exactly what
was and wasn't written, and carry on with the rest.

### Test runs

A test run uses client **Sandbox** (already an option in the Project Tracker) and a project name
like "Claude Launch Test". The user may name a variant such as "Sandbox-Mason": use it everywhere
(page titles, planner, folders, Slack) but set the tracker's Client property to "Sandbox". Use a
real past program's proposal as the strawman if the user names one — including its fee table for
the planner baseline (3a step 9). On a test run:
- Put the person running the skill in every people slot (BD DRI, TPL, Buddy) unless told otherwise.
- Calendar events: the runner is the only attendee; add "(TEST)" to titles and "TEST — safe to
  delete" to descriptions.
- Email drafts: addressed only to the runner, subject prefixed `[TEST]`.
- Slack: make the internal channel **private**; the #spanner-team win post is a **draft only**.
- Company lists (Step 3f): still written, marked TEST (see 3f).
- Harvest: set `HARVEST_USE_TEST_COPY=true` so the Provision script uses the COPY templates; invoice drafts get
  `[TEST]` in the subject and `SANDBOX TEST — DO NOT SEND.` in the notes.
- End the punch list with a cleanup list of everything created, with links.

## Important Context

A program launch is triggered when there is (a) a fully signed agreement, (b) a PO from the client,
or (c) a verbal agreement between the client and Spanner to launch.

The checklist has these sections, each detailed below:
1. Biz Dev wrap-up (BD)
2. Notion Project List (BD/TPL)
3. Project Planner setup (TPL)
4. Harvest setup (TPL)
5. Launch invoice (TPL)
6. Project folders (TPL)
7. Executive Summary and Dashboards
8. Slack channels (TPL)
9. Shared tools with client (TPL)
10. Meetings (TPL)
11. Launch Checklist Complete (TPL)

**Paste-ready text goes where it's used.** Anything the user has to copy into another app (invoice subject,
description, notes, PO number) goes into the Notion checklist item as `plain text` code blocks. Anything a
script reads (the agreement facts) goes into the planner. Never make the user open another file to find it.

---

## Step 0: Create the Project Page in Notion (Manual — Required First)

The project page and its launch checklist are created via a **Notion template button** on the
Active Projects page. This button lives at:

`https://www.notion.so/spannerpd/Active-Projects-ed1d7d57705d4767af8af87be34eda8d#1af7b5cbf3854c66ba94de35d7949e4b`

**Tell the user**: "Before I can automate the rest of the checklist, you need to click the
'New Project' button on the Active Projects page in Notion. This creates the project page and
launch checklist from the template. Once it's created, share the URL of the new project page
with me and I'll take it from there."

The template page is **locked** — ask the user to unlock the new page (••• menu → Unlock) when
they create it, or they won't be able to edit or move it later. (Claude's API edits work either way.)

The new page keeps the template's title, **including the `_Template_` prefix** (e.g.
"_Template_[Client] | [Project] | New Program Starter Kit @today") and the "Template page is Locked"
callout. That is expected — it is the new instance, not the template. Confirm by checking that it
sits under Active Projects and was just edited; the real template is linked at the bottom of
Active Projects ("DO NOT DUPLICATE THIS PAGE") and must never be renamed.

Wait for the user to provide the newly created project page URL. Use `notion-fetch` to read it
and extract whatever information was pre-populated by the template (title, child pages, etc.).
Also look for the launch checklist child page that was created alongside it.

Save both URLs:
- `PROJECT_PAGE_URL` — the main project page
- `CHECKLIST_PAGE_URL` — the BD-to-PD Launch Checklist child page

---

## Step 1: Gather Project Information

After the user has created the project page via the Notion button and shared the URL, collect
the remaining project details using AskUserQuestion. Ask in batches to avoid overwhelming
the user. You need:

### Batch 1 — Core details
- **Client name** — must match one of the existing clients in the Project Tracker, or be a new client name
- **Project name** — the full project name (e.g., "Gigamon | ME Design Support")
- **Project description** — a brief summary of the project
- **Program type** — T&M (Time & Materials) or Fixed Fee
- **Signed agreement and PO** — Drive links (the Harvest setup and deposit invoice are built from them)

### Batch 2 — People
- **BD DRI** — the Business Development person responsible (name or email)
- **TPL (Technical Program Lead)** — who will lead the project
- **Buddy** — the person providing close principal review and partnering with the TPL

### Batch 3 — Dates & Phases
- **Launch date** — when the project starts
- **End date** — anticipated end date (can be approximate)
- **Current phase** — one of: Phase 0 - Concept, Phase 1 - Definition, Phase 2 - Detail Design, Feasibility, Feasibility & Architecture, Engineering Support, Manufacturing Support, Concept Refinement, Strategic Assessment, Technology Development
- **Project phases planned** — which phases: Phase 0, Phase 1, Phase 2

### Batch 4 — Project-specific options
- **Referral bonus?** — Does this program qualify for a referral bonus/commission? (Yes/No/NA)
- **Uses contractors/partners?** — Will contractors or partners be involved? (Yes/No)
- **Client uses Gmail?** — Determines whether to create an external shared Google Drive (Yes/No)
- **Needs external Slack channel?** — Create a client-facing ext-CLIENTNAME-spanner channel? (Yes/No)
- **Needs shared CAD/whiteboard tools?** — Setup shared dev tools with client? (Yes/No)

---

## Step 2: Notion Setup (Automated)

### 2a. Rename and Populate the Project Page

The project page was already created in Step 0 via the Notion template button. Now:

1. Use `notion-fetch` on the `PROJECT_PAGE_URL` to see the current template content
2. Use `notion-update-page` to rename the page title to `{Client} | {Project Name}`
3. Update the page content to fill in project-specific details (links, team members, etc.)
   using `update_content` — find template placeholder text and replace it with real values

Also locate the launch checklist child page. It should have been created by the template
automatically. Use `notion-fetch` to confirm it exists and save its URL as `CHECKLIST_PAGE_URL`.

**Replace every `[Client]` / `[Project]` placeholder in the project's page tree.** The template
creates many subpages titled like `[Client] | [Project] | Team & Collaborators`. Find them with
`notion-search` (query `[Client] [Project]`, `page_url` = the project page, `page_size` 50; run a
second query `Client Project` to catch "Shared | Client | Project"-style titles). For every result
whose path is under this project page:
- **Pages** (`type: page`): rename with `notion-update-page` → `update_properties` → `title`,
  replacing `[Client]`/`Client` with `{Client}` and `[Project]`/`Project` with `{Project Name}`
  (e.g. `Shared | {Client} | {Project Name}`).
- **Databases** (results with `type: block`, e.g. Action Item List, EIL, Meetings and Project Notes,
  PRD Database, Phase 0 Checklists): rename under the **title-only exception to Safety Rule 1**.
  For each one: `notion-fetch` it, confirm the project page (`PROJECT_PAGE_URL`) is in its
  `ancestor-path` and its title contains `[Client]`/`[Project]`, take the `collection://` ID from
  its `<data-source>` tag, then call `notion-update-data-source` with **only** `data_source_id`
  and `title` (e.g. `{Client} | {Project Name} | EIL`). Keep the rest of the name as is; the icon
  is separate and stays. Never pass `statements`, `description`, `in_trash` or `is_inline`.
  (Proven 2026-09-29 on 5 databases; page templates and schemas were unchanged.)
- **Leave property names alone**, even ones that contain `Client | Project` (e.g. the relation
  "Client | Project | EIL"). Renaming them is a schema change and stays forbidden.
Re-run both searches afterwards and confirm no page or database titles still contain `[Client]`.

### 2b. Rename the Launch Checklist

Use `notion-update-page` to rename the checklist page (it already has the 🚀 icon — don't add
the emoji to the title):
- Title: `{Client} | {Project Name} | BD to PD Launch Checklist`

### 2c. Add to Program Launch Checklists "In Progress" section

The Program Launch Checklists page is at: `4eee597dc8c642078d44dbd5fe83d03a`

Use `notion-update-page` with command `update_content` to add a mention of the new checklist
page to the "In Progress" section:

```
old_str: "# In Progress {toggle=\"true\"}"
new_str: "# In Progress {toggle=\"true\"}\n\t<mention-page url=\"{CHECKLIST_PAGE_URL}\"/> "
```

Anchor on the heading line alone — matching an existing mention inside the section fails because
fetched URLs don't match the stored form. This puts the new checklist first in the section.

### 2d. Add Entry to Project Tracker Database

**⚠️ CRITICAL — READ-ONLY SCHEMA RULE:**
**NEVER use `notion-update-data-source` on the Project Tracker.** Do not ALTER, ADD, DROP,
or RENAME any columns. Do not modify the multi_select options. The `notion-create-pages` tool
automatically creates new multi_select options when you pass a value that doesn't exist yet —
no schema changes are needed or allowed. Modifying the schema with `ALTER COLUMN SET` on a
multi_select property **replaces all existing options**, which deletes every existing value
across all rows in the database. This is destructive and irreversible.

The Project Tracker data source is: `collection://efb9ea40-a2ae-4130-8d34-4cd0a39c8101`

Use `notion-create-pages` with parent `data_source_id: efb9ea40-a2ae-4130-8d34-4cd0a39c8101`:

Properties to set:
- `Name`: "{Client} | {Project Name}" (this is the title property)
- `Client`: JSON array, e.g. `["Gigamon"]` — the client name **must match an existing
  option** in the database. Before creating the entry, fetch the data source schema to
  get the current list of Client options and verify the client name exists. If the client
  is new and not in the options list, **do NOT use `notion-update-data-source` to add it**.
  Instead, tell the user: "The client '{name}' doesn't exist in the Project Tracker yet.
  Please add it manually in Notion (open the database, click a Client cell, type the new
  name, and press Enter), then let me know and I'll continue." Wait for confirmation
  before proceeding. This is the only safe way to add new multi_select options — using
  `notion-update-data-source` with ALTER COLUMN replaces ALL existing options and
  destroys data across every row.
- `Description`: project description text
- `Status`: "Kickoff Process"
- `Current Phase`: the selected phase
- `Project Phases`: JSON array of selected phases, e.g. `["Phase 0", "Phase 1"]`
- `Project Page`: URL of the project page created in step 2a
- `date:Launch Date:start`: launch date in ISO format
- `date:Launch Date:is_datetime`: 0
- `date:End Date:start`: end date in ISO format
- `date:End Date:is_datetime`: 0

Note: BD DRI, TPL, and Buddy are person properties requiring Notion user IDs. Search for users
using `notion-search` with `query_type: "user"` to find the right IDs, then set:
- `BD DRI`: JSON array of user IDs
- `TPL`: JSON array of user IDs
- `Buddy`: JSON array of user IDs

---

## Step 3: Google Drive Setup (Automated)

### 3a. Create Project Planner from Template

**Do NOT copy or read the Project Planner template via the Drive API** — Google flags it
"ineligible to be used in generative AI contexts", so API calls on it fail. The planner must be created
using the template's built-in Apps Script function. This ensures the client name, project name,
TPL, and other fields are properly populated throughout the spreadsheet.

The Project Planner template spreadsheet ID is: `1G4igU0bjZiR5xU7-_nT1JuhbC1Dd-ucjYjqGgAQth6I`

**Destination folder:** The planner is saved to the **Budget Forecast Tool** folder.
- Folder ID: `16b85a8ykDu4tPUDr7sttPuGrw_-zj_om`

**Process:**
1. Open the Project Planner **template** spreadsheet with the browser tool:
   `https://docs.google.com/spreadsheets/d/1G4igU0bjZiR5xU7-_nT1JuhbC1Dd-ucjYjqGgAQth6I/edit`
2. Wait for the custom menus to load (look for "Planner" in the menu bar)
3. If the "Authorize Scripts" button is visible or prompted, click it first and complete the OAuth flow
4. Click the orange **Click to create a new project** button on the template (same as
   **Planner** menu → **Create New Project...**). A "Project Setup" dialog opens.
5. Fill the dialog: **Client Name** `{Client}`, **Project Name** `{Project Name}`, **Phase Name**,
   **Duration (Weeks)**, **Engineering Budget ($)** and **Materials Budget ($)** from the
   agreement. Text fields accept typed input (click the field, then `type`).
   - **Launch Date must be set IN THE DIALOG.** The setup script uses it for more than B15 — in
     particular it sets the `weekOffset` cell (Sheet1 G28), which shifts the whole weekly chart.
     Setting B15 after creation leaves G28 wrong. Typing into the native date picker does not
     work; instead `find` "Launch Date" (the dialog is an iframe — `find`/`read_page` see into it)
     and use `form_input` on that ref with `YYYY-MM-DD`. If `form_input` doesn't stick, try JS in
     the dialog frame: set the input's `.value = 'YYYY-MM-DD'` and dispatch `input` and `change`
     events. Take a screenshot and confirm the date shows before clicking Create.
     (Not yet proven — first run to try it, report whether it worked.)
   - **Project Type** select: set it with `form_input` the same way (T&M or Fixed Fee).
   - If the launch date truly can't be set in the dialog, stop and ask the user to enter it in
     the dialog themselves before you click Create. Don't create the file and patch B15 later.
6. Click **Create Project File**, wait ~60s for "Success!", then click **Open Project Now**.
7. Capture the new planner URL from the tab info.
8. **Check and fix what the dialog doesn't set** (see Browser Automation Notes for the cell-edit
   method). Rows 7–24 are a collapsed group — expand it (the `+` left of row 6; click OK on the
   "Heads up" protection warning) before editing or reading them.
   - Verify `dateLaunch` (B15) shows the launch date and `weekOffset` (G28) is set. If the chart
     shows "PLEASE ENTER -1 IN CELL G28" or similar, the date didn't go in through the dialog —
     tell the user; don't hand-patch.
   - Named range `weeksInProject` (B14) must equal the agreement's duration in weeks. The
     dialog's **Duration (Weeks)** field sets it — always fill that field — and fix B14 if it
     doesn't match (e.g. the duration changed, or the field was left blank).
   - Also check `engineeringBudget` (B12) and `materialsBudget` (B13) match the agreement.
   - Named range `TPLName` (Sheet1 B8) — defaults to "TPLName"; set it to the TPL's first name
     as used in the __SUMMARY sheet's TPL column (e.g. "Mason", "Damien", "Niall").
   - **Approve the planner's own IMPORTRANGE links: Sheet1 `J1:L1`** ("Sheets Access" row; each
     shows `#REF!` until approved, and row 4 then reads "Approve Access Above"). Hover each
     `#REF!` cell and click **Allow access** until all three read TRUE. The cells sit to the right
     of the frozen columns, so use a wide viewport (Browser Automation Notes).
9. **Load the Baseline from the proposal's fee table** (Baseline Plan, rows ~36–44; one row per
   rate/role, week columns start where row 28 shows week `1`, i.e. the launch week):
   - Map each proposal line to the planner row with the same rate and the closest role
     (e.g. "Senior Mechanical Engineer $250" → `Sr PD` $250; "Principal / Exec $300" → `PR Exec`).
     If no row matches the rate, ask the user.
   - Enter the proposal's avg hrs/wk in each week column for that line's weeks, in sequence
     (e.g. 105 hrs/wk × 2 wks then 20 hrs/wk × 4 wks → 105,105,20,20,20,20).
   - Leave the other role rows as they are. Only rows with hours count as "used": they become the Harvest
     tasks, and the Harvest Create step moves them to the top of the baseline (Step 3.5).
   - **Verify:** D59 (Weekly Baseline Plan total) must equal the proposal's Engineering Subtotal
     and D58 the total hours. If not, stop and show the user the difference.
   - Estimated Forecast staffing (names) only with names from the user. Never assign
     contractors without the user confirming Giles approved.

After creation, verify the planner is in the Budget Forecast Tool folder (`16b85a8ykDu4tPUDr7sttPuGrw_-zj_om`)
by checking its metadata with `get_file_metadata`. If it was created elsewhere, tell the user to
move it to the Budget Forecast Tool folder.

Save the resulting planner URL — add it to the Notion project page links.

**Note**: The generated planner is named `{Client} | {Project Name} - Project Planner`.
Do not rename it manually — use the **Planner → Update File Name** menu option if a rename is needed.

**Important**: Remind the user:
- Do NOT add this on a Monday before Harvest approval is complete
- Unclick the BD checkbox (Cell F4) — this activates the planner for revenue forecasting
- Load staff in the Baseline and Estimated Forecast sections

### 3a-2. Add the Planner to the __SUMMARY Forecast Sheet

Add the new planner to **__SUMMARY Spanner Forecast / Budget Report Calculator**
(`1nLjHU0WUh-fYUA_Xvm61izUDFpG6TN8gN4Dpw1A4s1o`, tab **Combine**, gid `1287641798`).

- Put the planner URL in the first empty cell of the **ProjectURLs** named range (`Combine!B2:B47`).
  Every other column in that row is a pre-filled formula — do not touch them.
- Do not add rows beyond row 47 (formulas in BC2 depend on the range).
- After entering the URL, column C shows `#REF!` until the IMPORTRANGE link is approved: hover
  that cell and click **Allow access**. Within a few seconds the row fills in (#, client, project).
- Verify by reading `Combine!A{row}` / the rendered row.

### 3b. Generate Exec Summary Deck from the Project Planner

**The ONLY supported way to create the Exec Summary deck is the planner's built-in
Apps Script function — never copy a template deck.** The script creates the deck with all
charts and tables already linked to the planner data; no manual linking is needed afterward.

**Destination folder:** The exec summary is saved to the **00__Exec_Summaries** folder.
- Folder ID: `1h8PP0G6uEZ2PFbbRVN9_g29XvyPCEGx3`

**Process:**
1. Open the Project Planner spreadsheet (created in Step 3a) with the browser tool
2. Wait for the custom menus to load (look for "Planner" in the menu bar)
3. If the "Run Authorization" button is visible, click it first and complete the OAuth flow
4. Run **Planner** menu → **📊 Generate Exec Summary Deck** (not the "(Sandbox)" variant) —
   real clicks on the custom menu don't work; use the JS menu method in Browser Automation Notes.
5. Wait ~60s ("Building Deck" toast) — it creates a new Google Slides deck automatically
6. The new deck opens in a new tab; capture its URL and file ID from the tab info

After creation, verify the deck is in the 00__Exec_Summaries folder (`1h8PP0G6uEZ2PFbbRVN9_g29XvyPCEGx3`)
by checking its metadata with `get_file_metadata`. If it was created elsewhere, tell the user to
move it to the 00__Exec_Summaries folder.

Save the resulting deck URL and **file ID** (needed for the shortcut in Step 3c) — add the URL
to the Notion project page links.

**Note**: The generated deck is named `{Client} | {Project Name} - Project Exec Summary`
and is linked to pull data from the planner. Do not rename or move it. For subsequent data
refreshes, use **Planner → Update Exec Summary Deck** — never regenerate or re-link manually.

### 3c. Create Project Google Drive Folder (Copy from Template)

The project folder must be **copied from the template folder**, including all subfolders and
any documents inside them.

- **Studio > Projects folder ID:** `1lxV05VC_OR_Wcfmnosnr5xRGJQCrwu0q`
- **Template Folder Sample ID:** `10-q0XVsZvvjgCnElVAij_Dx4Ns4OHyB4`

**Process:**

1. **Create the top-level project folder:**
   Use `create_file` with:
   - `title`: `{Client} - {Project Name}`
   - `mimeType`: `application/vnd.google-apps.folder`
   - `parentId`: `1lxV05VC_OR_Wcfmnosnr5xRGJQCrwu0q`
   
   Save the new folder's ID — this is the `projectFolderId`.

2. **Recursively copy the template folder structure:**
   Walk the template folder tree and recreate it inside the new project folder. Use this
   recursive procedure:
   
   ```
   function copyFolderContents(templateFolderId, destinationFolderId):
     List all children of templateFolderId using search_files with parentId query
     For each child:
       If child is a folder (mimeType = application/vnd.google-apps.folder):
         Create a new folder with the same title inside destinationFolderId
         Recursively call copyFolderContents(child.id, newFolder.id)
       If child is a file (any other mimeType, including shortcuts):
         Use copy_file to copy the file with parentId = destinationFolderId
         and title = child.title (to avoid the default "Copy of" prefix)
   ```
   
   Start by calling: `copyFolderContents("10-q0XVsZvvjgCnElVAij_Dx4Ns4OHyB4", projectFolderId)`

3. **Create shortcuts in Program_Management (via the Drive website):**
   The Drive MCP can't create shortcuts, so do it in the browser:
   1. Open the folder holding the source file (for the deck: 00__Exec_Summaries,
      `https://drive.google.com/drive/folders/1h8PP0G6uEZ2PFbbRVN9_g29XvyPCEGx3`).
   2. `find` the file name, click it to select, then right-click the row → **Organize** →
      **Add shortcut** (hover Organize first; find "Add shortcut" to get its ref).
   3. In the dialog, the new project folder often is NOT under **Suggested**, and typing a
      folder name into the dialog's search doesn't work. What works: click the search icon, click
      the "Search folders or paste URL" field, `type` the **Program_Management folder's URL**
      (`https://drive.google.com/drive/folders/<id>`), press Return, click the one result, then
      click **Add**. A "Adding shortcut…" toast confirms.
   4. Verify with `search_files` (`parentId = '<Program_Management id>' and mimeType =
      'application/vnd.google-apps.shortcut'`).
   Do this for the Exec Summary deck, and for the signed agreement once it's archived (3e).

Save the project folder URL — add it to the Notion project page links.

### 3d. Create External Shared Drive (if client uses Gmail)

If the client uses Gmail, create an external shared Google Drive folder:
- `title`: `{CLIENT_NAME} | Spanner`
- `mimeType`: `application/vnd.google-apps.folder`

**Remind the user**:
- Set TPL permissions to Manager on the shared drive
- Ensure at least one or two other Spanner people have full rights

### 3e. Archive Signed Agreement

Ask the user for the fully signed agreement (Drive link or file). If they provide it:
- `copy_file` it into the Signed Agreements folder `1WdX33ToNSkRoIt5imdimEuKEHpCFmCS3` with
  title `Spanner_{Client}_{Project}_Proposal_Fully_Signed_YYMMDD` (YYMMDD = signing date)
- Add a shortcut to it in the project's Program_Management folder (3c step 3)
- Add the link to the Notion project page and check off the Agreement items
If no agreement is available yet, leave it on the punch list.

### 3f. Company Lists (shared resources)

These three updates are approved (Mason Curry, 2026-09-28) for every launch run, **including test
runs** (client "Sandbox"). They are company-wide files, so:
- Before writing, show the user exactly what will be added and where (one short list).
- On a test run, mark each entry so it's easy to clean up: append ` (TEST)` to the program
  name, and put `TEST entry - delete` in the case-study Notes column (J).
- If the session's permission system blocks the write, stop and tell the user which file and
  what was blocked — don't retry another way. Say exactly what state the file was left in
  (e.g. an inserted but empty row).

1. **Future case studies list** (`1BLZsjKLweZF1T22vuhEq-zr7wqBMRnieVwTYllqaeCU`, Sheet1).
   Rows are alphabetical by Client (col B). Columns: A Priority, B Client, C TPL,
   D Calendar Year, E On SpannerPD Website, F Program(s), G Public Link, H Client ask,
   I What we did, J Notes, K Collateral located.
   - **Don't insert a row.** Add the entry in the first empty row at the bottom of the list
     (read col B via the name box to find the last filled row), then **sort by Client**:
     use the filter on the header row (row 3) → Client (col B) → **Sort A → Z**, so the whole
     filtered table re-sorts together. (Not yet proven — verify after.)
   - Fill B (client), C (TPL first name), D (launch year), F (project name); H if the
     proposal summary is available; J only for test runs. Leave the rest blank.
   - Fill the row completely before sorting. After the sort, read col B around the client's
     alphabetical position and confirm the new row landed there with all its cells intact.
2. **Project rate tracker** (Notion `448dc1dfe5c64845904daf600a34eeb6`, "Rates for Active
   Programs"). Add one line with the program name under **# Fixed Fee Programs** or the
   current **# T/M … Rates** heading, in alphabetical position, matching the existing style
   (e.g. "Feno - HW V2 Def/Arch Sprint"). Note any non-standard rate the user mentions.
3. **DATA STACK Allow Access** (`1dfJ0J06Vcj9d1CY4Hv4WTpEcJr_JCzAgmGBiwG_TlUM`, range B1): open
   it, find the new planner's `#REF!` cell, hover it and click **Allow access** — same as
   the __SUMMARY sheet in 3a-2.

Status as of v1.7.1 (2026-09-28 Sandbox-Mason run): the case-study row fill, the rate-tracker
line, DATA STACK Allow access and __SUMMARY Allow access are all proven. The append-then-sort
method for item 1 is new and not yet proven — verify after writing and report what you see.

---

## Step 3.5: Harvest Setup (script creates, Claude prepares and verifies)

Harvest is created by the **ProjectMaster Provision script** from the planner, never by hand-duplicating
the template and never by Claude writing projects directly. Claude prepares the inputs and checks the result
with the **Harvest MCP** (read tools + draft invoices). The user clicks **Create**.

**One-time setup (already done 2026-09-29; don't repeat):** the library holds the Harvest OAuth app
(ID/secret/redirect in Script Properties, set via the Provision menu's admin prompts), and the
"Harvest OAuth callback" web-app deployment. Each user connects once via Development WIP → 🔐 Authorize Harvest.
Planners need `userinfo.email` in their manifest and the three stubs (`showHarvestProvisionDialog`,
`harvest_provisionPreview`, `harvest_provisionConfirm`) — the planner template has them from 2026-09-29.

### 3.5a Write the agreement facts into the planner
Extract from the signed agreement (header table + Program Fees table) and the PO, then write the JSON into the
planner's **Harvest Setup** tab, cell **A3** (create the tab if missing; A1 = label). The user never pastes it.
Shape (Gigamon example in `spanner-apps-script/_fixtures/harvest-provision/gigamon_agreement.json`):
`{title, date, signed, type, engBudget, materialsEst, depositEng, depositMat, netDays, billing, weeks, link,
fees:[{role, hrsWk, rate, weeks}], po:{number, date, netDays, link}}`
- `signed`: leave null if the agreement has no date — the script uses the PO date.
- `depositEng`/`depositMat`: from the agreement header ("Deposit $38,950 ($38,950 eng + $0 materials)").
- Writing it (browser): if the tab is missing, click **＋** (bottom-left) to add a sheet, rename it `Harvest Setup`
  (right-click the tab → Rename), then put the one-line JSON in A3 with the name-box cell method (Browser Automation
  Notes). Read it back. If writing fails, the dialog also has the box — give the user the JSON in chat as a last resort.
- Script-side (not yet proven live, 2026-09-29): the dialog loads A3, and Create saves the box back to A3.

### 3.5b Check with the Harvest MCP before Create
- `list_clients` / `list_projects` — client exists? project already exists (don't duplicate)?
- `list_project_assignments` on the template (HOURLY `25028609`, INTERVAL `27125057`; test copies
  `49282400` / `49282410` when `HARVEST_USE_TEST_COPY=true`) — tasks, rates, team.

### 3.5c User runs the preview and Create
Planner → Development WIP → **🌾 Provision Harvest Project (preview)…**. The preview loads the Harvest Setup JSON.
The user checks it, ticks any 🛑 acknowledgement (e.g. agreement Net 30 vs PO Net 45), and clicks **Create in Harvest**.
What the script does:
- Creates the project from the template (T&M, bill by task, cost budget = engineering budget, dates, notes filled
  from the agreement/PO), and copies the template team (all flagged manager).
- **Tasks = only baseline roles with hours** (plus their `NB - ` task). Role → task map: Sr PD / Senior Mechanical
  Engineer → Sr. Product Development; SR EE / SR FW → Sr. Product Development - EE/FW; PR Exec / PR ME / PR EE /
  Principal / Exec → Principal; TPL → Technical Program Lead; PD → Product Development; CTO → CTO.
  Harvest's auto-added default tasks and all unused roles are removed.
- Writes the Harvest ID to B10 and **moves the baseline rows with hours to the top** (unused rows stay below, unchanged).
  Only columns that are plain values in every baseline row move; a column mixing formulas and values stops the sort.
  (Tested on mock data only, 2026-09-29 — check the baseline after the first real run.)

### 3.5d Verify, then finish
- `list_project_assignments` (tasks + users) and `get_project_budget` on the new ID; compare to the preview.
- Remove any stray task with `remove_task_from_project` only if the user approves.
- Add the Harvest link to the Notion project page; check off the Harvest items on the checklist.
- Invoice values (PO number, due-date terms) are **manual in Harvest** — the API can't set them. Put the paste-ready
  values in the checklist's Harvest item (code blocks).

---

## Step 4: Slack Setup (Automated)

### 4a. Create Internal Project Channel

Create it with `slack_create_conversation` (`channel_name`, `is_private` as the user prefers;
always private on test runs):
- Internal channel: `{client-name-lowercase}-{project-short-name}`
- External channel (if needed): `ext-{client-name-lowercase}-spanner` — **must be private**
If the connector refuses, give the user the exact names to create manually.

### 4b. Post Launch Announcement

Once channels exist (or if the user provides the channel name), use `slack_send_message` to post
a launch announcement in the internal channel with key project details.

---

## Step 5: Google Calendar Setup (Automated)

### 5a. Set Up Weekly Exec Reviews

Use `create_event` to create a recurring weekly meeting:
- `summary`: `{Client} | {Project Name} - Exec Review`
- `startTime` / `endTime`: default Monday afternoon, 30 minutes (the checklist standard); confirm
  with the user. Include a Week 1 instance.
- `recurrenceData`: `["RRULE:FREQ=WEEKLY;UNTIL={end date}T235959Z"]`
- `description`: Include links to Exec Summary deck and Project Planner
- Include a Google Meet URL: set `addGoogleMeetUrl: true`
- Add attendees as needed (TPL, Buddy, and optionally execs like Giles and Arne)

### 5b. Schedule BD-PD Internal Kickoff

Use `create_event` for a one-time meeting:
- `summary`: `{Client} | {Project Name} - BD-PD Internal Kickoff`
- `description`: "BD DRI to convey objectives, deliverables, and nuances. Full PD team mandatory."
- Ask user for date/time
- Attendees: BD DRI (mandatory), full PD team (mandatory), Giles and Arne (optional)

### 5c. Schedule Client Kickoff

Use `create_event` for a one-time meeting:
- `summary`: `{Client} | {Project Name} - Client Kickoff`
- Ask user for date/time and client attendee emails
- Attendees: PD team + client contacts, Giles and Arne (optional)

---

## Step 6: Notifications (Automated)

### 6a. Program Win Announcement (Slack #spanner-team)

The win announcement goes to **#spanner-team** (channel ID `C02PJEL2T5L`) as a Slack message —
not an email. Show the user the text and post with `slack_send_message` only after they say yes;
otherwise save it with `slack_send_message_draft` so they can send it themselves. For test runs,
always draft, never post.

Format (match the team's existing launch posts):
- Opener: `:rocket: We're launching a new {program type} program for {Client}: {one-line summary}.`
- Key dates, TPL / BD DRI / Buddy, contractors if any
- Referral bonus if applicable ($1,000 per client referral, minimum $20k eng program; paid in the
  first pay cycle after launch)
- Link to the Notion project page

### 6b-0. Draft the deposit invoice in Harvest (Harvest MCP)

After the Harvest project exists, create the launch invoice as a **draft** with `create_invoice` (drafts can't be sent
through the MCP; never send). T&M: the agreement's Deposit. FF: Payment 1.
- `client_id`: the project's client; `issue_date`: today; `payment_term`: `upon receipt` (agreement Deposit Net 0)
- `purchase_order`: the PO number
- `subject`: `Product Development and Engineering | {Project} | Launch Deposit` (prefix `[TEST] ` on test runs)
- one line item: `kind` **`Launch Deposit`**, `description` `Launch Deposit — Engineering ({pct}% of ${engBudget} estimate)`,
  `quantity` 1, `unit_price` deposit, `project_id` the new project
- `notes`: `Engineering deposit per agreement dated {date}: ${depositEng} ({pct}% of ${engBudget} engineering estimate) + ${depositMat} materials. Applied 50% against the first invoice and 50% against the second.`
  (test runs: start with `SANDBOX TEST — DO NOT SEND.`)
- The MCP **can't edit invoices**. Verify with `get_invoice`; anything wrong is fixed by the user in Harvest.
- Add a checklist item under **Launch invoice**: "Review and update the draft invoice in Harvest", with the subject,
  description, PO number and notes in `plain text` code blocks, the due date, and "Type: Launch Deposit".

### 6b. Draft Launch Invoice Request

Use `create_draft` to draft the invoice request:
- `to`: [Karina's email — ask user to confirm]
- `cc`: [TPL, Arne, Giles, Mason, Torence — ask for emails or use known addresses]
- `subject`: `Launch Invoice Request: {Client} | {Project Name}`
- `body`:
  - For T&M programs: "Please prepare the Deposit invoice as designated on page 1 of the agreement"
  - For FF programs: "Please prepare Payment 1 as designated in the payment schedule"
  - Include project name, client, and TPL contact, and the Harvest draft invoice number from 6b-0

### 6c. Draft Contractor Forecast Notification (if applicable)

If the program uses contractors/partners, use `create_draft`:
- `to`: [Karina's email]
- `cc`: [Giles, Arne, Torence, Mason, and TPL]
- `subject`: `Contractor/Partner Forecast: {Client} | {Project Name}`
- `body`: "Please see the attached contractor/partner forecast hours for this program."
- **Remind the user** to attach a screenshot of the planner forecast before sending

---

## Step 7: Update Notion Project Page with All Links

After all resources are created, go back and update the project page (step 2a) with all the
generated links using `notion-update-page`:

- Project Planner link
- Exec Summary link
- Google Drive folder link
- External shared drive link (if created)
- Harvest link (`https://spannerpd.harvestapp.com/projects/{id}` after Create)

---

## Step 8: Manual Steps Punch List

After completing all automated steps, present a clear punch list of remaining manual tasks.
Format this as a checklist the user can work through:

List only what's still open — drop anything Claude completed in this run.

### Must Do Now (always the user's)
- [ ] **Tag opportunity as Won** in the BD pipeline
- [ ] **Update BD Pipeline Bookings/Win sheet** with the new booking
- [ ] Any Step 3e/3f item that couldn't be completed
- [ ] On test runs: list every TEST entry written (case studies row, rate tracker line, __SUMMARY row, Harvest test project and draft invoice) so the user can delete them

### Notion
- [ ] Any project database still titled `[Client] | [Project]` (only if the title-only rename failed — list by name)

### Project Planner Setup
- [ ] **Unclick BD checkbox** (Cell F4) — this activates the planner for revenue forecasting
- [ ] **Load staff** in the Baseline section (only if Claude couldn't load it from the proposal)
- [ ] **Load staff** in the Estimated Forecast section as Pending (note PR, TPL, PD, SPD roles)
- [ ] **Loop Giles in** before assigning any contractors to the program

### Harvest Setup
- [ ] **Run Planner → Development WIP → 🌾 Provision Harvest Project (preview)…** and click Create (only if not done)
- [ ] **Set Invoice values by hand** in Harvest (PO number, due-date terms) — values are in the checklist
- [ ] **Review the draft deposit invoice** in Harvest (Type = Launch Deposit) — values are in the checklist
- [ ] For Fixed Fee: confirm payment plan with BD DRI in Harvest
- [ ] Note any subbed contractors/partners and their budgets

### Shared Tools (if applicable)
- [ ] Set up CAD sharing, whiteboard, or other shared dev tools with the client

### Drafts to Send
- [ ] **Review and send** the #spanner-team win post (if left as a Slack draft)
- [ ] **Review and send** the launch invoice request draft
- [ ] **Review and send** the contractor forecast notification (if applicable) — attach forecast screenshot first

### Final Steps (gated — see Close-out Rule)
- [ ] Move the Launch Checklist to the "Completed" section of [Program Launch Checklists](https://www.notion.so/4eee597dc8c642078d44dbd5fe83d03a)
- [ ] Change the Project Tracker status from "Kickoff Process" to "In Progress"

---

## Execution Flow

When running this skill, follow this sequence:

0. **Create project page** (Step 0) — Instruct user to click the Notion template button, then collect the new page URL
1. **Gather info** (Step 1) — Use AskUserQuestion in 2-3 batches
2. **Search for Notion users** — Look up BD DRI, TPL, and Buddy user IDs
3. **Populate Notion pages** (Step 2) — Rename project page, all `[Client] | [Project]` subpages & the checklist, populate tracker entry, add to launch checklists
4. **Set up Google Drive** (Step 3) — Create Planner via template script with launch date, duration and budgets set in the dialog (saved to Budget Forecast Tool folder), check B12–B15 and G28, set TPL, approve J1:L1, load the Baseline from the proposal, add it to the __SUMMARY ProjectURLs range, generate Exec Summary deck via Planner → Generate Exec Summary Deck (saved to 00__Exec_Summaries folder), copy template folder structure to Studio > Projects, add exec summary shortcut to project's Program_Management folder, archive the signed agreement if provided (3e), then the company lists (3f)
4b. **Set up Harvest** (Step 3.5) — Write agreement JSON to the planner's Harvest Setup tab, MCP pre-checks, user clicks Create, MCP verify, add Harvest link
5. **Set up Slack** (Step 4) — Create channels or instruct user
6. **Set up Calendar** (Step 5) — Ask for meeting times, then create events
7. **Notifications** (Step 6) — draft deposit invoice in Harvest (6b-0), #spanner-team win post, invoice request draft, contractor forecast draft
8. **Update Notion with links** (Step 7) — Add all generated links back to the project page
9. **Present manual punch list** (Step 8) — Clear summary of what's left

After each major step, report what was created with links so the user can verify.

**Never do these — they stay with the user:** clicking **Create** in the Harvest Provision dialog, editing
Harvest outside the approved steps (Claude may only: read via the MCP, draft the deposit invoice, and remove stray
tasks on the new project with approval), sending any invoice, the BD Pipeline Bookings/Win sheet, and sending any
email (Gmail items stay as drafts).

**Close-out Rule**: Only move the checklist to Completed and set the tracker to "In Progress"
when every item on the checklist is checked (done or N/A). Before doing it, `notion-fetch` the
checklist and count `- [ ]`; if any remain, list them and stop. Never close out in the same run
as launch setup unless that count is zero, and ask the user before closing out.

**Checklist management**: As each step completes, check off the corresponding item on the
launch checklist in Notion using `notion-update-page` with `update_content`. If a checklist
item does not apply to this project (e.g., no contractors, no external Slack channel, client
doesn't use Gmail), check it off as well — do not leave non-applicable items unchecked.

---

## Key Reference IDs

These IDs are used throughout the automation:

### Notion
| Resource | ID |
|---|---|
| Active Projects page | `ed1d7d57705d4767af8af87be34eda8d` |
| Project Tracker data source | `collection://efb9ea40-a2ae-4130-8d34-4cd0a39c8101` |
| Program Launch Checklists page | `4eee597dc8c642078d44dbd5fe83d03a` |
| Launch Checklist template (inside the New Program Starter Kit `7584270bccb24ef981788f753d5b7a5c`) | `360222a7d409813c944dd96202b81bce` |
| Tin Launch Checklist template (Tin client projects) | `2ede8162d2ee4d7280255efa151c657c` |
| Project rate tracker | `448dc1dfe5c64845904daf600a34eeb6` |

### Google Drive
| Resource | File ID |
|---|---|
| Project Planner template | `1G4igU0bjZiR5xU7-_nT1JuhbC1Dd-ucjYjqGgAQth6I` |
| Template Folder Sample | `10-q0XVsZvvjgCnElVAij_Dx4Ns4OHyB4` |
| Studio > Projects folder | `1lxV05VC_OR_Wcfmnosnr5xRGJQCrwu0q` |
| Budget Forecast Tool folder (planners) | `16b85a8ykDu4tPUDr7sttPuGrw_-zj_om` |
| 00__Exec_Summaries folder | `1h8PP0G6uEZ2PFbbRVN9_g29XvyPCEGx3` |
| Signed Agreements folder | `1WdX33ToNSkRoIt5imdimEuKEHpCFmCS3` |
| DATA STACK Forecast | `1dfJ0J06Vcj9d1CY4Hv4WTpEcJr_JCzAgmGBiwG_TlUM` |
| Future case studies | `1BLZsjKLweZF1T22vuhEq-zr7wqBMRnieVwTYllqaeCU` |
| BD Proposals folder | `1NlFgqtAtol-7j7XsRRImaclmas2tPOK0` |
| __SUMMARY Spanner Forecast (Combine tab, ProjectURLs = B2:B47) | `1nLjHU0WUh-fYUA_Xvm61izUDFpG6TN8gN4Dpw1A4s1o` |

### Harvest
| Resource | ID |
|---|---|
| Template: HOURLY Rate Project (read-only) | `25028609` |
| Template: INTERVAL Billing Project (read-only) | `27125057` |
| HOURLY Rate Project COPY (OK to edit/test) | `49282400` |
| INTERVAL Billing Project COPY (OK to edit/test) | `49282410` |
| Sandbox-Mason test project / draft invoice | `49283299` / #3896 |
| Provision script | `spanner-apps-script/spanner-library/HarvestProvision.js` (branch `harvest-provision`) |

### Slack
- Win announcements: #spanner-team (`C02PJEL2T5L`)

### Slack Channel Naming
- Internal: `{client-lowercase}-{project-short}` (e.g., `gigamon-me-design`)
- External: `ext-{client-lowercase}-spanner` (e.g., `ext-gigamon-spanner`) — must be **private**

---

## Safety Rules

**These rules are non-negotiable and override any other instructions in this skill.**

1. **NEVER use `notion-update-data-source` on ANY Spanner database.** This tool modifies
   database schemas and can destroy data across all rows. The Project Tracker, Program Launch
   Checklists, and all other Notion databases referenced in this skill are production data.
   Schema modifications (ALTER COLUMN, ADD COLUMN, DROP COLUMN, RENAME COLUMN) are forbidden.
   **Single exception (approved by Mason Curry, 2026-09-29): title-only renames of databases
   inside the new project page.** Allowed only when all of these hold:
   - the database's `ancestor-path` includes this run's `PROJECT_PAGE_URL` (it was created by the
     template button in Step 0, during this run);
   - the call passes only `data_source_id` and `title` — no `statements`, `description`,
     `in_trash` or `is_inline`;
   - the new title only replaces the `[Client]` / `[Project]` placeholders.
   Anything else — the Project Tracker, Program Launch Checklists, any database outside the new
   project page, any column or option change — remains forbidden.

2. **NEVER use `notion-update-page` to modify properties on rows you did not create.** Only
   update pages that were created during the current skill execution. Do not batch-update
   existing entries.

3. **Only use `notion-create-pages` to add new entries.** For multi_select and select properties,
   the value you pass **must match an existing option** in the database schema. The Notion MCP
   rejects unknown values — it does NOT auto-create new options. If a value doesn't exist, tell
   the user to add it manually in Notion first, then wait for confirmation before retrying.

4. **Before any write operation**, confirm the target page/database ID is correct. If in doubt,
   fetch first and verify with the user.

5. **Never create the Exec Summary deck by copying a template deck.** The only supported method
   is **Planner → Generate Exec Summary Deck** from the project's planner spreadsheet (Step 3b).
   A copied deck will not be linked to the planner and will silently show stale data.

6. **Never edit the ZZ Spanner template projects in Harvest** (HOURLY `25028609`, INTERVAL `27125057`).
   Only the COPY projects may be edited for testing. Never send an invoice.

---

## Error Handling

- If a Notion user search returns no results, ask the user for the correct name/email
- If a Google Drive copy fails, provide the template URL so the user can copy manually
- If Slack channel creation isn't supported by the connector, provide exact names for manual creation
- Always verify created resources by fetching them after creation
- If any step fails, continue with the remaining steps and note the failure in the final punch list
- Planner script error **"Library with identifier ProjectMaster is missing"**: the user lacks access
  to the planner's Apps Script library. Stop the planner steps and ask them to get access from the
  planner owner (Mason Curry); everything else can continue.
- Notion page can't be edited or moved by the user: it's still locked from the template — they
  unlock it via ••• → Unlock.
- Harvest Provision errors: "Specified permissions are not sufficient to call Session.getActiveUser" → the planner's
  manifest lacks `userinfo.email` (add it via clasp). "Not Configured" → the Provision menu's admin setup runs
  (Mason only). "function not found" → the planner lacks the three Provision stubs (add via clasp).

---

## Browser Automation Notes (built-in browser + Google Sheets)

Learned on the 2026-09-28 test runs (incl. Sandbox-Mason | Scout ME Design Support, v1.7.1). Use these instead of rediscovering them.

- **Sign-in / auth**: Google may show "Verify it's you" — the user must sign in; never enter
  credentials. If Apps Script OAuth ("Authorize Scripts" / "Run Authorization") won't complete in
  the built-in browser, ask the user to open the planner in their own browser (Safari/Chrome), run
  **Planner → 🔑 Authorize Scripts** once there, then reload in the built-in browser — the scripts
  then run from it. This is one-time per person.
- **Custom menus (Planner, Spanner_Tools)** aren't in menu search and real clicks on the menubar
  miss. Open the menu with JS, highlight the item with JS, then press a real Return:
  ```js
  const m=[...document.querySelectorAll('.menu-button')].find(x=>x.textContent.trim()==='Planner');
  ['mousedown','mouseup'].forEach(t=>m.dispatchEvent(new MouseEvent(t,{bubbles:true,view:window})));
  // wait ~1s, then:
  const it=[...document.querySelectorAll('.goog-menuitem')].find(x=>x.offsetParent&&x.textContent.includes('Generate Exec Summary Deck')&&!x.textContent.includes('Sandbox'));
  it.dispatchEvent(new MouseEvent('mouseover',{bubbles:true,view:window}));
  ```
  then `computer key Return`.
- **Editing a cell — preferred, coordinate-free (proven 2026-09-28):**
  1. JS: navigate with the name box (set `#t-name-box` via `execCommand('insertText')`, dispatch an
     Enter keydown, wait ~800 ms).
  2. Real `Return` key → the cell enters edit mode.
  3. JS: check `#t-name-box` is the intended cell, then
     `document.execCommand('selectAll'); document.execCommand('insertText', false, VALUE)`.
     **Always guard on the name-box value** — if it doesn't match, write nothing.
  4. Real `Tab` (or `Return`) to commit.
  For consecutive cells in a row: commit with `Tab`, press `Return` to edit the next cell, repeat.
  To skip a cell, press `Tab` without `Return`. Verify every write by reading it back.
  - Fallback: real **double-click** on the cell (fresh screenshot for coordinates) instead of
    steps 1–2. Coordinates break under viewport emulation, so don't combine the two.
  - To read a cell: name-box navigation as above, then read `#t-formula-bar-input`. Reads can lag
    right after a structural change (row insert) — wait and re-read before trusting them.
- **Allow access (IMPORTRANGE `#REF!`)**: hover the `#REF!` cell (or select it via the name box)
  so the "You need to connect these spreadsheets" card appears, then do a **real click** on its
  **Allow access** button. JS-dispatched clicks on `div.jfk-button` sometimes work and sometimes
  don't; if a JS click leaves `#REF!`, use a real click. The card can open off-screen at the
  bottom of the narrow pane — widen the viewport. Approving one planner link can resolve its
  siblings too; re-read before clicking again.
- **Row groups**: the planner hides rows 7–24 (and 45–57, 72–85) in collapsed groups. Name-box
  navigation to a hidden row silently lands on the next visible row — expand the group first.
- **New planner authorization**: the first script run on each new planner shows "Authorization
  required" even if the template was authorized. OAuth consent is the user's to approve — ask them,
  then reload and re-run the menu item.
- **Custom menu item didn't run** (no "Running script" toast within a few seconds): the JS
  highlight + Return missed. Take a screenshot — the menu is usually still open — and click the
  item with a real click.
- Screenshots of the pane can lag; trust JS reads of the name box / formula bar over pixels.
- **Viewport**: the built-in pane is narrow, and the planner's frozen columns A–G fill it, so the
  week columns (H onward) and J1:L1 are invisible. `resize_window` 1600×1600 shows them. Real
  single clicks (e.g. Allow access) worked at 1600×1000; a double-click at 1600×1600 landed on the
  wrong cell, so edit cells with the name-box method while emulating. Reset to `desktop` when done.
- **Screenshots from the user** land in `~/Documents/Screenshots for Claude` with a narrow no-break space before
  AM/PM in the file name; staging by that name fails. Copy them to ASCII names in a `_claude-copies` subfolder first.
