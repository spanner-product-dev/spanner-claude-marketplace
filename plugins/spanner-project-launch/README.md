# Spanner Project Launch Plugin

Automates the Spanner BD-to-PD Launch Checklist for new projects.

## What it does

When you say "launch a new project" or "new project setup", this skill walks through the full BD-to-PD checklist:

1. Creates Notion pages (Program Launch Checklist, Project Tracker entry)
2. Creates Google Drive folder structure (copied from template folder with all subfolders and docs)
3. Creates Project Planner (saved to Budget Forecast Tool folder)
4. Generates Exec Summary deck (saved to 00__Exec_Summaries folder, with shortcut in project's Program_Management)
5. Sets up Harvest project with budgets and tasks
6. Creates Slack channel and posts intro message
7. Creates Google Calendar kickoff meeting
8. Sends notification emails
9. Logs the run to the Spanner Project Launch Log sheet

## Safety

This plugin includes strict safety rules to prevent accidental data loss in Notion databases. It will never modify database schemas or existing entries it didn't create.

## Version History

- **1.5.0** — Removed all remnants of the old exec-deck template-copy method (template deck ID, obsolete "link deck to planner" and "Dashboard 4" punch-list items) — the deck is generated exclusively via the Planner → Generate Exec Summary Deck script. Added Step 9: every run is logged as a row in the Spanner Project Launch Log Google Sheet.
- **1.4.0** — Updated Google Drive workflow: project folder is now copied from template folder (including all subfolders and documents); planner destination documented as Budget Forecast Tool folder; exec summary destination documented as 00__Exec_Summaries folder; added exec summary shortcut in Program_Management (manual step).
- **1.3.0** — Fixed Safety Rules to correctly document that Notion MCP does NOT auto-create multi_select options.
- **1.2.0** — Added Safety Rules section preventing destructive schema modifications.
- **1.1.0** — Added Harvest integration with OAuth2 authentication.
- **1.0.0** — Initial release.
