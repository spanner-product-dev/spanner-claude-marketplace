# Spanner Project Launch Plugin

Automates the Spanner BD-to-PD Launch Checklist for new projects.

## What it does

When you say "launch a new project" or "new project setup", this skill walks through the full BD-to-PD checklist:

1. Creates Notion pages (renames the project page and Launch Checklist, adds the Project Tracker entry, links the checklist under In Progress)
2. Creates the Project Planner via the template's Apps Script dialog (launch date, duration and budgets set in the dialog; Budget Forecast Tool folder), sets the TPL, approves the planner's IMPORTRANGE links and loads the Baseline from the proposal
3. Adds the planner to the __SUMMARY Spanner Forecast ProjectURLs range and approves its IMPORTRANGE link
4. Generates the Exec Summary deck via Planner → Generate Exec Summary Deck (00__Exec_Summaries folder)
5. Copies the project folder from the template and adds Program_Management shortcuts (deck, signed agreement) via the Drive website
6. Archives the signed agreement when provided
7. Updates the company lists: Future Case Studies sheet (append, then sort by client), Rates for Active Programs (Notion), DATA STACK Allow access
8. Creates the internal Slack channel and drafts/posts the #spanner-team win announcement
9. Creates Google Calendar exec review and kickoff meetings
10. Drafts the launch invoice and contractor forecast emails (never sends)
11. Hands back a punch list; closes out the checklist only when every item is checked
12. Sets up Harvest through the planner's **🌾 Provision Harvest Project** script (you click Create): only baseline roles with hours become tasks, used baseline rows move to the top, the Harvest ID goes into the planner. Claude checks the result with the Harvest MCP and drafts the launch deposit invoice (drafts only)

It never clicks Create in Harvest for you, never sends an invoice or email, and never touches the BD Pipeline Bookings/Win sheet or the ZZ Spanner template projects.

## Safety

This plugin includes strict safety rules to prevent accidental data loss in Notion databases. It will never modify database schemas or existing entries it didn't create.

## Version History

- **1.9.0** — **SpannerOS:** new Step 3.6. After Harvest Create, the project is imported into SpannerOS **staging** with the planner repo's single-project importer (`--harvest-project`). The run goes pre-check → dry run → user OK → commit, and a new client code needs the user's approval. TPL, phase, PO and payment terms are then set by a one-row SQL update, the planner is registered for planner sync, and the result is verified. If the Cowork shell can't reach Harvest/Supabase, the user runs the command in Terminal. Adds Safety Rule 7: staging only, one row, no prod. **Also, from the 2026-09-30 Timeless Way run with Torence:** a **BD (pre-launch) mode**: with no signature, PO or verbal go, look for an existing [BD] planner first, keep F4 checked, use Agreement # PENDING, link the proposal in Harvest (paste-ready notes fix), and skip the win post, Slack drafts and invoice drafts until signing. Planner launch date: press the keys one at a time. Full-week baselines even for mid-week launches. Header rows 34–35 never move (library fix pushed). Check the Harvest end date after Create. Stop on `showHarvestProvisionDialog` not found and hand off to clasp. Exec deck: confirm the highlighted menu item isn't the (Sandbox) variant. Tin launches use the Tin checklist button. Spanner must be the default Google account (`/u/0`).
- **1.8.0** — From the 2026-09-29 Sandbox-Mason run (also includes the unreleased 1.7 changes). **Harvest:** new Step 3.5 — agreement facts go in the planner's Harvest Setup tab, the ProjectMaster Provision script creates the project (Harvest tasks = baseline roles with hours plus their NB tasks; used baseline rows moved to the top; payment-terms conflicts must be acknowledged), Claude verifies with the Harvest MCP; new 6b-0 drafts the launch deposit invoice (item type Launch Deposit) and puts paste-ready invoice text in the checklist. Harvest reference IDs and a never-edit-the-templates rule. **Planner:** launch date, duration and budgets set in the setup dialog (so G28 weekOffset is right), B14 weeks check, J1:L1 IMPORTRANGE approval, Baseline loaded from the proposal fee table. **Notion:** all `[Client] | [Project]` subpages renamed, plus a title-only exception for renaming databases inside the new project page. Case-studies list: append then sort instead of inserting a row. Browser notes for the coordinate-free cell edit method and wide viewport.
- **1.6.0** — From the 2026-09-28 test run. Win announcement moved from email to a #spanner-team Slack post. Launch Log step removed. Added: __SUMMARY ProjectURLs row, planner launch-date/TPL fix, Drive-website shortcuts, signed-agreement archive, company-list updates (case studies, rate tracker, DATA STACK) including on test runs, gated close-out rule, explicit never-do list (Harvest, BD bookings, sending email), Paul dropped from invoice cc, Browser Automation Notes for Google Sheets/Apps Script menus, a Before You Start section (connectors, sign-in, permission prompts), test-run conventions, and troubleshooting for the locked template page and the ProjectMaster library error. The skill is now self-contained — no per-user memory needed to run it.
- **1.5.0** — Removed all remnants of the old exec-deck template-copy method (template deck ID, obsolete "link deck to planner" and "Dashboard 4" punch-list items) — the deck is generated exclusively via the Planner → Generate Exec Summary Deck script. Added Step 9: every run is logged as a row in the Spanner Project Launch Log Google Sheet.
- **1.4.0** — Updated Google Drive workflow: project folder is now copied from template folder (including all subfolders and documents); planner destination documented as Budget Forecast Tool folder; exec summary destination documented as 00__Exec_Summaries folder; added exec summary shortcut in Program_Management (manual step).
- **1.3.0** — Fixed Safety Rules to correctly document that Notion MCP does NOT auto-create multi_select options.
- **1.2.0** — Added Safety Rules section preventing destructive schema modifications.
- **1.1.0** — Added Harvest integration with OAuth2 authentication.
- **1.0.0** — Initial release.
