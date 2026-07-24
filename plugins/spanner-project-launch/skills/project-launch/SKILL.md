---
name: project-launch
description: >
  Automate the Spanner BD-to-PD Launch Checklist for new projects. Use this skill whenever someone says
  "launch a new project", "new project setup", "BD to PD checklist", "project kickoff", "set up a new program",
  "start a new project", "program launch", "launch checklist", "new client project", "kickoff checklist",
  or any variation of starting the BD-to-PD transition process. Also use when someone asks to
  "automate project setup", "run the launch checklist", or references the BD-PD launch process.
  This skill creates Notion pages, Project Tracker entries, Google Drive folders and templates,
  Slack channels, Google Calendar meetings, and notification emails — then
  provides a punch list for the remaining manual steps.
---

# Spanner BD-to-PD Project Launch Automation

This skill automates the BD-to-PD Launch Checklist that Spanner runs for every new project. It handles
setup across Notion, Google Drive, Slack, Google Calendar, and Gmail, then gives clear instructions
for the steps that still need a human.

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

---

## Step 0: Create the Project Page in Notion (Manual — Required First)

The project page and its launch checklist are created via a **Notion template button** on the
Active Projects page. This button lives at:

`https://www.notion.so/spannerpd/Active-Projects-ed1d7d57705d4767af8af87be34eda8d#1af7b5cbf3854c66ba94de35d7949e4b`

**Tell the user**: "Before I can automate the rest of the checklist, you need to click the
'New Project' button on the Active Projects page in Notion. This creates the project page and
launch checklist from the template. Once it's created, share the URL of the new project page
with me and I'll take it from there."

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

### 2b. Rename the Launch Checklist

Use `notion-update-page` to rename the checklist page:
- Title: `🚀 {Client} {Project Name} | BD to PD Launch Checklist`

### 2c. Add to Program Launch Checklists "In Progress" section

The Program Launch Checklists page is at: `4eee597dc8c642078d44dbd5fe83d03a`

Use `notion-update-page` with command `update_content` to add a mention of the new checklist
page to the "In Progress" section:

```
old_str: "# In Progress {toggle=\"true\"}"
new_str: "# In Progress {toggle=\"true\"}\n\t<mention-page url=\"{new_checklist_page_url}\"/> "
```

Wait — this may not work if the In Progress section already has content. Instead, add the mention
right after the toggle header line, before the first existing mention.

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

**Do NOT copy the Project Planner template via the Drive API.** The planner must be created
using the template's built-in Apps Script function. This ensures the client name, project name,
TPL, and other fields are properly populated throughout the spreadsheet.

The Project Planner template spreadsheet ID is: `1G4igU0bjZiR5xU7-_nT1JuhbC1Dd-ucjYjqGgAQth6I`

**Destination folder:** The planner is saved to the **Budget Forecast Tool** folder.
- Folder ID: `16b85a8ykDu4tPUDr7sttPuGrw_-zj_om`

**Process:**
1. Open the Project Planner **template** spreadsheet in Chrome using the browser tools:
   `https://docs.google.com/spreadsheets/d/1G4igU0bjZiR5xU7-_nT1JuhbC1Dd-ucjYjqGgAQth6I/edit`
2. Wait for the custom menus to load (look for "Planner" in the menu bar)
3. If the "Authorize Scripts" button is visible or prompted, click it first and complete the OAuth flow
4. Click: **Planner** menu → **Create New Project...**
5. The script will prompt for:
   - **Client name** — enter `{Client}` (from the Notion Project Tracker entry)
   - **Project name** — enter `{Project Name}` (from the Notion Project Tracker entry)
6. Wait for the script to complete — it will create a new Project Planner spreadsheet with all
   fields (client, project name, TPL, launch date, etc.) properly populated
7. The new planner opens in a new tab; capture its URL from the tab info

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

### 3b. Generate Exec Summary Deck from the Project Planner

**The ONLY supported way to create the Exec Summary deck is the planner's built-in
Apps Script function — never copy a template deck.** The script creates the deck with all
charts and tables already linked to the planner data; no manual linking is needed afterward.

**Destination folder:** The exec summary is saved to the **00__Exec_Summaries** folder.
- Folder ID: `1h8PP0G6uEZ2PFbbRVN9_g29XvyPCEGx3`

**Process:**
1. Open the Project Planner spreadsheet (created in Step 3a) in Chrome using the browser tools
2. Wait for the custom menus to load (look for "Planner" in the menu bar)
3. If the "Run Authorization" button is visible, click it first and complete the OAuth flow
4. Click: **Planner** menu → **Generate Exec Summary Deck**
5. Wait for the script to complete — it will create a new Google Slides deck automatically
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

3. **Create Exec Summary shortcut in Program_Management:**
   After the folder structure is copied, locate the `Program_Management` subfolder inside the
   new project folder (it was created in step 2). The Drive MCP does not support creating
   shortcuts (mime type `application/vnd.google-apps.shortcut`), so tell the user:
   
   "Please create a shortcut to the Exec Summary deck in the project's Program_Management
   folder. In Google Drive, right-click the deck in 00__Exec_Summaries → Organize → Add
   shortcut → navigate to the project's Program_Management folder."

Save the project folder URL — add it to the Notion project page links.

### 3d. Create External Shared Drive (if client uses Gmail)

If the client uses Gmail, create an external shared Google Drive folder:
- `title`: `{CLIENT_NAME} | Spanner`
- `mimeType`: `application/vnd.google-apps.folder`

**Remind the user**:
- Set TPL permissions to Manager on the shared drive
- Ensure at least one or two other Spanner people have full rights

### 3e. Archive Signed Agreement

**Remind the user** to:
- Archive the signed agreement in the Signed Agreements drive: `1WdX33ToNSkRoIt5imdimEuKEHpCFmCS3`
- Use filename format: `Spanner_{Client}_{Project}_Proposal_Fully_Signed_YYMMDD`
- Add the link to the Notion project page

---

## Step 4: Slack Setup (Automated)

### 4a. Create Internal Project Channel

Use `slack_send_message` to the user — actually, Slack channel creation may need to be done
through the Slack UI since the connector may not support channel creation directly.

**If channel creation is available**: Create a channel named `{client-name-lowercase}-{project-short-name}`

**If not available**: Tell the user to create:
- Internal channel: `{client-name-lowercase}-{project-short-name}` (can be public or private)
- External channel (if needed): `ext-{client-name-lowercase}-spanner` (must be private, not public)

### 4b. Post Launch Announcement

Once channels exist (or if the user provides the channel name), use `slack_send_message` to post
a launch announcement in the internal channel with key project details.

---

## Step 5: Google Calendar Setup (Automated)

### 5a. Set Up Weekly Exec Reviews

Use `create_event` to create a recurring weekly meeting:
- `summary`: `{Client} | {Project Name} - Exec Review`
- `startTime` / `endTime`: Ask the user for preferred day/time, default to 30 minutes
- `recurrenceData`: `["RRULE:FREQ=WEEKLY"]`
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

### 6a. Draft Program Win Email

Use `create_draft` to draft the win email:
- `to`: [ask user for team distribution list email, or send to known team addresses]
- `subject`: `🎉 Program Win: {Client} | {Project Name}`
- `body`: Include program summary, key dates, team assignments, and referral bonus info if applicable
  - Referral bonus: $1,000 per client referral, minimum $20k eng program
  - Timing: tied to first pay cycle after program launch

### 6b. Draft Launch Invoice Request

Use `create_draft` to draft the invoice request:
- `to`: [Karina's email — ask user to confirm]
- `cc`: [TPL, Arne, Giles, Mason, Paul, Torence — ask for emails or use known addresses]
- `subject`: `Launch Invoice Request: {Client} | {Project Name}`
- `body`:
  - For T&M programs: "Please prepare the Deposit invoice as designated on page 1 of the agreement"
  - For FF programs: "Please prepare Payment 1 as designated in the payment schedule"
  - Include project name, client, and TPL contact

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
- Harvest link (remind user to add after manual setup)

---

## Step 8: Log the Launch Run (Automated)

Every run of this skill is logged as a row in the **Spanner Project Launch Log** Google Sheet:

- Sheet ID: `1adbCIuS-EyVsnLiMwP143xDFGgSqV239TIHNAr4l6Mw`
- URL: `https://docs.google.com/spreadsheets/d/1adbCIuS-EyVsnLiMwP143xDFGgSqV239TIHNAr4l6Mw/edit`

Columns (in order):
`Run Date | Client | Project | TPL | Program Type | Planner URL | Exec Deck URL | Project Folder URL | Notion Project Page | Run By | Notes`

**Process:**
1. Open the log sheet in Chrome using the browser tools
2. Click the first empty row and enter one value per column, in the order above:
   - **Run Date**: today's date, `YYYY-MM-DD`
   - **Client / Project / TPL / Program Type**: from Step 1
   - **Planner URL / Exec Deck URL / Project Folder URL**: from Step 3 (leave blank if a step failed)
   - **Notion Project Page**: `PROJECT_PAGE_URL`
   - **Run By**: the user running the skill
   - **Notes**: anything unusual — skipped steps, failures, partial runs
3. Verify the row was saved (Sheets autosaves; confirm the values appear in the row)

**Log partial runs too.** If the launch was aborted or some steps failed, still add the row and
record what happened in Notes — the log is only useful if it captures every run, not just clean ones.

**Fallback:** If browser tools are unavailable, give the user the sheet URL and the exact
row values to paste in manually, formatted as a single tab-separated line.

---

## Step 9: Manual Steps Punch List

After completing all automated steps, present a clear punch list of remaining manual tasks.
Format this as a checklist the user can work through:

### Must Do Now
- [ ] **Tag opportunity as Won** in the BD pipeline
- [ ] **Update BD Pipeline Bookings/Win sheet** with the new booking
- [ ] **Archive the signed agreement** to the Signed Agreements drive (folder ID: `1WdX33ToNSkRoIt5imdimEuKEHpCFmCS3`)
  - Filename: `Spanner_{Client}_{Project}_Proposal_Fully_Signed_YYMMDD`
- [ ] **Add program to the project rate tracker** (Notion page: `/448dc1dfe5c64845904daf600a34eeb6`)
- [ ] **Add program to the future case studies list**: [Google Sheet](https://docs.google.com/spreadsheets/d/1BLZsjKLweZF1T22vuhEq-zr7wqBMRnieVwTYllqaeCU/edit#gid=0)

### Project Planner Setup
- [ ] **Unclick BD checkbox** (Cell F4) — this activates the planner for revenue forecasting
- [ ] **Load staff** in the Baseline section
- [ ] **Load staff** in the Estimated Forecast section as Pending (note PR, TPL, PD, SPD roles)
- [ ] **Loop Giles in** before assigning any contractors to the program
- [ ] **Allow Access** in the [DATA STACK Spanner Forecast/Budget Report](https://docs.google.com/spreadsheets/d/1dfJ0J06Vcj9d1CY4Hv4WTpEcJr_JCzAgmGBiwG_TlUM/edit?gid=1900729131#gid=1900729131&range=B1)

### Harvest Setup
- [ ] **Create Harvest project** using the Harvest API Data Hub or directly in Harvest
  - Use the ZZ Spanner template (HOURLY Rate or INTERVAL Billing)
  - Set client, project name, budget, hourly rate, dates, and team members
  - [How-to video](https://www.notion.so/spannerpd/Harvest-Setup-fbc4f28b198148cdb8b7c68f9ef9c951)
  - [Setup instructions](https://www.notion.so/fbc4f28b198148cdb8b7c68f9ef9c951)
- [ ] For Fixed Fee: confirm payment plan with BD DRI in Harvest
- [ ] Note any subbed contractors/partners and their budgets
- [ ] **Add HarvestID** to the Project Planner
- [ ] **Add Harvest link** to the Notion project page

### Shared Tools (if applicable)
- [ ] Set up CAD sharing, whiteboard, or other shared dev tools with the client

### Email Drafts
- [ ] **Review and send** the program win email draft
- [ ] **Review and send** the launch invoice request draft
- [ ] **Review and send** the contractor forecast notification (if applicable) — attach forecast screenshot first

### Final Steps
- [ ] Once all steps are complete, the Launch Checklist page should be moved to the "Completed" section of the [Program Launch Checklists](https://www.notion.so/4eee597dc8c642078d44dbd5fe83d03a) page
- [ ] Change the project status in the Project Tracker from "Kickoff Process" to "In Progress"

---

## Execution Flow

When running this skill, follow this sequence:

0. **Create project page** (Step 0) — Instruct user to click the Notion template button, then collect the new page URL
1. **Gather info** (Step 1) — Use AskUserQuestion in 2-3 batches
2. **Search for Notion users** — Look up BD DRI, TPL, and Buddy user IDs
3. **Populate Notion pages** (Step 2) — Rename project page & checklist, populate tracker entry, add to launch checklists
4. **Set up Google Drive** (Step 3) — Create Planner via template script (saved to Budget Forecast Tool folder), generate Exec Summary deck via Planner → Generate Exec Summary Deck (saved to 00__Exec_Summaries folder), copy template folder structure to Studio > Projects, add exec summary shortcut to project's Program_Management folder
5. **Set up Slack** (Step 4) — Create channels or instruct user
6. **Set up Calendar** (Step 5) — Ask for meeting times, then create events
7. **Draft emails** (Step 6) — Win email, invoice request, contractor notification
8. **Update Notion with links** (Step 7) — Add all generated links back to the project page
9. **Log the run** (Step 8) — Append a row to the Spanner Project Launch Log sheet (even for partial runs)
10. **Present manual punch list** (Step 9) — Clear summary of what's left

After each major step, report what was created with links so the user can verify.

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
| Launch Checklist template | `35ace833d8a14c1fb4cc722849914406` |
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
| Spanner Project Launch Log | `1adbCIuS-EyVsnLiMwP143xDFGgSqV239TIHNAr4l6Mw` |
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

---

## Error Handling

- If a Notion user search returns no results, ask the user for the correct name/email
- If a Google Drive copy fails, provide the template URL so the user can copy manually
- If Slack channel creation isn't supported by the connector, provide exact names for manual creation
- Always verify created resources by fetching them after creation
- If any step fails, continue with the remaining steps and note the failure in the final punch list — and still log the run in the Launch Log (Step 8) with the failures in Notes
