# Spanner Claude marketplace

A Claude Code plugin marketplace for Spanner Product Development. Publish this directory as a Git repo (e.g. `spanner-product-dev/spanner-claude-marketplace`) so every teammate can install Spanner's Claude Code plugins.

## Plugins
| Plugin | What it does |
|---|---|
| `spanner-security` | Spanner's secure-by-default engineering standard as an always-on skill. |
| ~~`spanner-toolkit`~~ | **Retired as a plugin 2026-09-18** — it was skills only, and every one of its skills is in the claude.ai Skills library. Two copies of the same guidance drift apart; that is how `spanneros-crud-scaffolder` spent four months recommending a UI library the project does not use. **The skill FILES still live at `plugins/spanner-toolkit/skills/` and are still the source of truth** — only the plugin packaging is gone. |
| ~~`spanner-project-launch`~~ | **Retired as a plugin 2026-09-18**, same reasoning. Its skill is `project-launch` in the Skills library. |

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

**Setting this up from scratch, or handing it to someone else? Read `SKILLS-RUNBOOK.md`.**
It is the step-by-step, assumes no prior knowledge of these files, and covers what is
currently wrong and how to fix it.

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

## How many skills to turn on — fewer than you think

**The limit is RECALL, not tokens.** Anthropic's enterprise guidance is explicit: *"limit the
number of Skills loaded simultaneously to maintain reliable recall accuracy. Each Skill's metadata
competes for attention in the system prompt. With too many Skills active, Claude may fail to select
the right Skill or miss relevant ones entirely."* So "it is only a description, leave it on" is the
wrong instinct — an always-on skill that is rarely relevant makes the relevant ones harder to find.

The documented pattern is **role-based bundles**: keep each person's ACTIVE set small, and let
everything else be discoverable but off.

| Tier | Skills | Why |
|---|---|---|
| **Required** — on, cannot be disabled | `spanner-security-standard` | It is a standard. Its whole value is that nobody has to remember to invoke it, and nobody can opt out. |
| **Installed by default** — on, removable | `spanner-operating-model`, `spanner-brand-voice`, `spanner-brand-visual` | Everyone answers "how does Spanner work" and everyone writes or reviews something client-facing. Three is a deliberately short list. |
| **Available to install** — discoverable, off | everything else | Real skills, but role-specific. Someone who never writes a migration should not be carrying `spanneros-schema-migration` in every conversation. |

**Available to install is not a demotion.** It means the skill appears in the directory and a person
switches it on in one click. The engineering set — `spanneros-crud-scaffolder`,
`spanneros-schema-migration`, `spanner-apps-script`, `torque-design-language`,
`spanner-internal-deploy`, `spanner-domain-ssl-dns` — is used by one or two people, so it belongs
here rather than in everyone's context.

If your plan supports per-group targeting, use it: give the engineering group the build skills by
default instead of making them self-install.

## For teammates — install (per user)
```
/plugin marketplace add spanner-product-dev/spanner-claude-marketplace
/plugin install spanner-security@spanner
```

## For the org — enforce for everyone (recommended)
Push the plugin to every machine via Claude Code **managed settings** so no one has to install it by
hand. `install-spanner-security.sh` in this repo writes that file; it needs sudo and is run once per
Mac:

```
curl -fsSL https://raw.githubusercontent.com/spanner-product-dev/spanner-claude-marketplace/main/install-spanner-security.sh | sudo bash
```

**That reaches only the Macs it is run on.** The alternative, which needs nobody's terminal, is to
register this marketplace under claude.ai → Organization settings → Plugins → *Organization library*
and set `spanner-security` to **Required**. Prefer that. See `SKILLS-RUNBOOK.md` §8.2 — as of
2026-09-18 the secret gate is confirmed on exactly one machine, which is not what the security
standard claims.

## For a single repo — enable per-project
Commit a `.claude/settings.json` to the repo:
```json
{
  "enabledPlugins": { "spanner-security@spanner": true }
}
```
(Collaborators still need the marketplace added; managed settings avoids that.)
