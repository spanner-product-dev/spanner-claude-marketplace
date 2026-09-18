# Spanner Claude marketplace

A Claude Code plugin marketplace for Spanner Product Development. Publish this directory as a Git repo (e.g. `spanner-product-dev/spanner-claude-marketplace`) so every teammate can install Spanner's Claude Code plugins.

## Plugins
| Plugin | What it does |
|---|---|
| `spanner-security` | Spanner's secure-by-default engineering standard as an always-on skill. |
| `spanner-toolkit` | Spanner's working skill set for Claude Code — project setup, Apps Script/clasp guardrails, SpannerOS migrations/CRUD scaffolding, Torque UI, design loop, operating model, portal deploy, domain/SSL/DNS, weekly digest, matrix sync, meeting notes. |
| `spanner-project-launch` | Automates the BD-to-PD Launch Checklist — Notion tracker entry, planner + exec deck (via planner scripts), Drive folders, Slack, Calendar, email drafts, run logging, and the manual punch list. |

## Source of truth — read this before editing a skill anywhere else

**Every Spanner skill is authored here, in `plugins/<plugin>/skills/<skill>/`.** This repo is the
only place a skill should be edited: it has history, diffs and PR review, and none of the other
copies do.

Everything else is a **publish target**, not a source:

| Copy | What it is | How it gets updated |
|---|---|---|
| **This repo** | the source of truth | PR → `main` |
| **Org settings** (claude.ai → Capabilities → Skills) | what most people actually load | **manual upload** — run `scripts/export-skills-for-org.sh` |
| **`~/.claude/plugins/cache/spanner/…`** | a local cache of the plugin | auto, on `autoUpdate`. **Never edit — it is overwritten silently** |
| **`~/.claude/plugins/marketplaces/spanner`** | a git checkout of this repo | `git pull`. It can fall behind while the cache is current, so pull before editing |

```
./scripts/export-skills-for-org.sh      # regenerates dist/org-settings (gitignored)
```

**Publishing to org settings is a manual step and will be forgotten.** On 2026-09-18 the
org-settings copy of `spanneros-schema-migration` was found to be twelve migrations behind, and
`spanneros-crud-scaffolder` was telling Claude to use shadcn/ui in a project that deliberately has
none — actively wrong, not merely stale. **After merging a skill change, upload it.** A skill that
contradicts the codebase costs more than no skill at all.

### One skill has a source ABOVE this repo

`spanner-security-standard` derives from `SpannerOS/Security Framework/spanner-security-standard.md`
in Drive, and its own `references/full-standard.md` says that document wins on disagreement. So a
security change goes **Drive first, then here, then org settings** — three hops, and the reason the
skill states the precedence in its own text rather than relying on anyone remembering it.

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
