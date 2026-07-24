# Spanner Claude marketplace

A Claude Code plugin marketplace for Spanner Product Development. Publish this directory as a Git repo (e.g. `spanner-product-dev/spanner-claude-marketplace`) so every teammate can install Spanner's Claude Code plugins.

## Plugins
| Plugin | What it does |
|---|---|
| `spanner-security` | Spanner's secure-by-default engineering standard as an always-on skill. |
| `spanner-toolkit` | Spanner's working skill set for Claude Code — project setup, Apps Script/clasp guardrails, SpannerOS migrations/CRUD scaffolding, Torque UI, design loop, operating model, portal deploy, domain/SSL/DNS, weekly digest, matrix sync, meeting notes. |
| `spanner-project-launch` | Automates the BD-to-PD Launch Checklist — Notion tracker entry, planner + exec deck (via planner scripts), Drive folders, Slack, Calendar, email drafts, run logging, and the manual punch list. |

## For teammates — install (per user)
```
/plugin marketplace add spanner-product-dev/spanner-claude-marketplace
/plugin install spanner-security@spanner
```

## For the org — enforce for everyone (recommended)
Push the plugin to every machine via Claude Code **managed settings** so no one has to install it by hand. See `../ROLLOUT.md` for the exact file and JSON.

## For a single repo — enable per-project
Commit a `.claude/settings.json` to the repo:
```json
{
  "enabledPlugins": { "spanner-security@spanner": true }
}
```
(Collaborators still need the marketplace added; managed settings avoids that.)
