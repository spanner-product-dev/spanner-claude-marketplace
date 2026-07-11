# Spanner Claude marketplace

A Claude Code plugin marketplace for Spanner Product Development. Publish this directory as a Git repo (e.g. `spanner-product-dev/spanner-claude-marketplace`) so every teammate can install Spanner's Claude Code plugins.

## Plugins
| Plugin | What it does |
|---|---|
| `spanner-security` | Spanner's secure-by-default engineering standard as an always-on skill. |

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
