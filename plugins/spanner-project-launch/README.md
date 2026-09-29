# Spanner Project Launch Plugin

Automates the Spanner BD-to-PD Launch Checklist for new projects.

## What it does

When you say "launch a new project" or "new project setup", this skill walks through the full BD-to-PD checklist:

1. Creates Notion pages (renames the project page and Launch Checklist, adds the Project Tracker entry, links the checklist under In Progress)
2. Creates the Project Planner via the template's Apps Script dialog (Budget Forecast Tool folder), then fixes the launch date and TPL the dialog can't set
3. Adds the planner to the __SUMMARY Spanner Forecast ProjectURLs range and approves its IMPORTRANGE link
4. Generates the Exec Summary deck via Planner → Generate Exec Summary Deck (00__Exec_Summaries folder)
5. Copies the project folder from the template and adds Program_Management shortcuts (deck, signed agreement) via the Drive website
6. Archives the signed agreement when provided
7. Updates the company lists: Future Case Studies sheet, Rates for Active Programs (Notion), DATA STACK Allow access
8. Creates the internal Slack channel and drafts/posts the #spanner-team win announcement
9. Creates Google Calendar exec review and kickoff meetings
10. Drafts the launch invoice and contractor forecast emails (never sends)
11. Hands back a punch list; closes out the checklist only when every item is checked

It never touches Harvest, the BD Pipeline Bookings/Win sheet, or sends email.

## Safety

This plugin includes strict safety rules to prevent accidental data loss in Notion databases. It will never modify database schemas or existing entries it didn't create.

## Version History

- **1.6.0** — From the 2026-09-28 test run. Win announcement moved from email to a #spanner-team Slack post. Launch Log step removed. Added: __SUMMARY ProjectURLs row, planner launch-date/TPL fix, Drive-website shortcuts, signed-agreement archive, company-list updates (case studies, rate tracker, DATA STACK) including on test runs, gated close-out rule, explicit never-do list (Harvest, BD bookings, sending email), Paul dropped from invoice cc, Browser Automation Notes for Google Sheets/Apps Script menus, a Before You Start section (connectors, sign-in, permission prompts), test-run conventions, and troubleshooting for the locked template page and the ProjectMaster library error. The skill is now self-contained — no per-user memory needed to run it.
- **1.5.0** — Removed all remnants of the old exec-deck template-copy method (template deck ID, obsolete "link deck to planner" and "Dashboard 4" punch-list items) — the deck is generated exclusively via the Planner → Generate Exec Summary Deck script. Added Step 9: every run is logged as a row in the Spanner Project Launch Log Google Sheet.
- **1.4.0** — Updated Google Drive workflow: project folder is now copied from template folder (including all subfolders and documents); planner destination documented as Budget Forecast Tool folder; exec summary destination documented as 00__Exec_Summaries folder; added exec summary shortcut in Program_Management (manual step).
- **1.3.0** — Fixed Safety Rules to correctly document that Notion MCP does NOT auto-create multi_select options.
- **1.2.0** — Added Safety Rules section preventing destructive schema modifications.
- **1.1.0** — Added Harvest integration with OAuth2 authentication.
- **1.0.0** — Initial release.
