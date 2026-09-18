# Spanner skills — the setup runbook

**Who this is for:** someone sitting down at Mason's Mac who has never seen these files, does not
know how Claude skills work, and needs to get this into a good state. No prior knowledge assumed.

**How long:** about 90 minutes end to end. Part 3 (uploading) is the slow bit because it is manual
clicking, and there is no way around that today.

**What you need before you start:**

- Admin (Owner) access to the Spanner Claude organization at [claude.ai](https://claude.ai)
- Push access to `spanner-product-dev/spanner-claude-marketplace` on GitHub
- Access to Mason's personal GitHub account `mcspan`, **or** Mason available to run two commands
- The `gh` CLI signed in (`gh auth status` should say Logged in)
- Sudo on the Mac, for one step in Part 5

---

# 1 · Orientation — what these things are

Read this even if you are in a hurry. Most of the mess below comes from people not knowing the
difference between these three words.

### A skill

A folder containing `SKILL.md` — plain Markdown telling Claude how to do something specific, plus
optionally a `references/` subfolder with longer documents it can pull in. Claude reads only the
**name and description** at first; the body is loaded only when the skill looks relevant. That is
why descriptions matter so much and why the count matters (see *recall*, below).

### A plugin

A bundle. It can contain skills, **and also things a skill cannot be**: hooks (code that runs
automatically on an event), slash commands, and MCP servers. If a bundle contains only skills, it
does not need to be a plugin at all.

**Spanner has exactly one thing that genuinely needs to be a plugin:** `spanner-security`, which
carries a `PreToolUse` hook that scans for secrets before any Bash command runs. Everything else is
skills wearing a plugin costume.

### The three places a skill can live

| Place | What it is | Who sees it |
|---|---|---|
| **This Git repo** | the source of truth — where skills are authored and reviewed | whoever reads GitHub |
| **claude.ai org settings** | the Skills library | **everyone in the org, in every Claude surface** |
| **A local plugin cache** (`~/.claude/plugins/cache/…`) | an auto-updating copy of a plugin | only that one Mac, only in Claude Code |

**These do not sync.** Anthropic documents this plainly: *"Custom Skills do not sync across
surfaces… Each surface requires separate uploads and management… implement your own synchronization
process."* That "own synchronization process" is `scripts/export-skills-for-org.sh` in this repo.

### Recall — why you cannot just turn everything on

Anthropic's enterprise guidance: *"limit the number of Skills loaded simultaneously to maintain
reliable recall accuracy. Each Skill's metadata competes for attention in the system prompt. With
too many Skills active, Claude may fail to select the right Skill or miss relevant ones entirely."*

So the cost of an always-on skill is not tokens. It is that it makes the *other* skills harder for
Claude to find. Keep the always-on set short.

### Added vs Published — the thing that confuses everyone

They are two different **routes in**, not two stages.

- **Added** = an owner uploaded it directly in org settings. Available to the org.
- **Published** = a member submitted it with *Publish to org* and an owner approved it under the
  **Requests** tab.

Both end up in the same Library list. The badge tells you how it arrived, not how widely it is
deployed. **Deployment is the separate dropdown** on the right of each row:

| Setting | Meaning |
|---|---|
| **Required** | On for everyone. Nobody can turn it off. |
| **Installed by default** | On for everyone. A person can turn it off. |
| **Available to install** | Off, but visible in the directory. One click to enable. |
| **Not available** | Hidden. Nobody sees it. |

---

# 2 · What is wrong right now

Do not skip this. Several steps below only make sense once you know what you are fixing.

### Problem A — two sources of truth, on two different GitHub accounts

There are **two** marketplaces feeding Spanner skills:

| Marketplace | GitHub repo | Owned by |
|---|---|---|
| `spanner` | `spanner-product-dev/spanner-claude-marketplace` | **the org** ✅ |
| `spanner-plugins` | `mcspan/spanner-plugins` | **Mason personally** ⚠️ |

The personal one holds four skills, two of which also exist in the org repo:

| Skill | In org repo | In personal repo | State |
|---|---|---|---|
| `spanner-brand-visual` | — | ✅ | **only copy is in a personal account** |
| `spanner-brand-voice` | — | ✅ | **only copy is in a personal account** |
| `spanner-design-loop` | ✅ 274 lines | ✅ 262 lines | **two sources, already drifted** |
| `spanner-internal-deploy` | ✅ | ✅ | two sources, identical today |

`spanner-brand-visual` and `spanner-brand-voice` are used across the company and exist only in one
person's private GitHub. That is the highest-priority item in this document.

### Problem B — two org skills are out of date, one of them harmfully

| Skill | Org settings copy says | Reality |
|---|---|---|
| `spanneros-crud-scaffolder` | *"Next.js App Router + TypeScript + Supabase + **shadcn/ui** + zod"* | The project **has no component library**. This copy makes Claude write components that do not belong. **Actively wrong.** |
| `spanneros-schema-migration` | *"especially for writing `002_schema_updates.sql`"* | Migrations are at **042**. The current version has a verify-script contract and RLS performance rules this copy has never heard of. **~4 months stale.** |

### Problem C — three skills exist in the repo and have never been uploaded

`spanner-apps-script`, `torque-design-language`, `matrix-task-sync`. Nobody in the org can use them.

### Problem D — two plugins that should not be plugins

The org Plugins page shows *Spanner brand* and *Spanner project launch*, both **Installed by
default**. Neither contains a hook, a command or an MCP server — they are skills only, and their
skills **also** exist in the Skills library. So people carry two copies of the same guidance, which
can drift apart independently. That is exactly how Problem B happened.

### Problem E — a README pointing at a file that does not exist

`README.md` references `../ROLLOUT.md`. There is no such file.

---

# 3 · The target state

When you are done:

- **One** source of truth: `spanner-product-dev/spanner-claude-marketplace`.
- **One** plugin: `spanner-security`, carrying the secret-gate hook and nothing else.
- **16 skills** in the claude.ai Skills library, with a deliberate access tier on each.
- The personal `mcspan/spanner-plugins` marketplace retired.
- A repeatable publish step anyone can run.

---

# 4 · Part 1 — consolidate the two repos into one

**Goal:** move the four brand skills into the org repo so there is one place to edit them.

### 1.1 Get both repos current

```bash
cd ~/.claude/plugins/marketplaces/spanner && git checkout main && git pull --ff-only origin main
```

```bash
cd ~/.claude/plugins/marketplaces/spanner-plugins && git checkout main && git pull --ff-only origin main
```

> **Trap:** these local checkouts can sit **behind** origin while the plugin *cache* is current — on
> 2026-09-18 the `spanner` checkout was 18 commits behind and editing it would have silently
> reverted a rewrite. Always pull first. Never edit anything under
> `~/.claude/plugins/cache/` — that folder is overwritten without warning.

### 1.2 Compare the two copies of the skills that exist in both

```bash
diff ~/.claude/plugins/marketplaces/spanner-plugins/spanner-brand/skills/spanner-design-loop/SKILL.md \
     ~/.claude/plugins/marketplaces/spanner/plugins/spanner-toolkit/skills/spanner-design-loop/SKILL.md
```

Read the diff and decide which is correct — **do not assume the longer one wins.** Ask Mason if it
is not obvious. Repeat for `spanner-internal-deploy` (identical as of 2026-09-18, so expect no
output).

### 1.3 Copy the two brand skills into the org repo

```bash
cd ~/.claude/plugins/marketplaces/spanner && git checkout -b chore/absorb-brand-skills
```

```bash
cp -R ~/.claude/plugins/marketplaces/spanner-plugins/spanner-brand/skills/spanner-brand-visual \
      ~/.claude/plugins/marketplaces/spanner-plugins/spanner-brand/skills/spanner-brand-voice \
      ~/.claude/plugins/marketplaces/spanner/plugins/spanner-toolkit/skills/
```

If step 1.2 showed the personal copy of `spanner-design-loop` is the better one, copy it across too.

### 1.4 Commit, push, PR, merge

```bash
cd ~/.claude/plugins/marketplaces/spanner && git add -A && git commit -m "chore: absorb the brand skills from the personal marketplace" && git push -u origin chore/absorb-brand-skills
```

```bash
cd ~/.claude/plugins/marketplaces/spanner && gh pr create --fill && gh pr merge --squash --delete-branch
```

### 1.5 Retire the personal marketplace — LAST, and not before the merge

Only once the skills are safely in the org repo. In claude.ai → **Organization settings → Plugins**,
remove the *Spanner brand* plugin. Then on the Mac:

```bash
rm -rf ~/.claude/plugins/marketplaces/spanner-plugins
```

**Do not delete the GitHub repo `mcspan/spanner-plugins`.** Leave it as a dormant backup for a few
months. Add a line to its README saying it has moved, so nobody edits it by mistake.

---

# 5 · Part 2 — reduce to one plugin

**Goal:** stop shipping skills-only plugins that duplicate the Skills library.

### 2.1 Remove the skills-only plugins from the marketplace manifest

Edit `.claude-plugin/marketplace.json` and delete the `spanner-toolkit` and
`spanner-project-launch` entries from the `plugins` array. **Leave `spanner-security`.**

**Leave the folders under `plugins/` alone.** The skills still live there and
`scripts/export-skills-for-org.sh` still reads them. You are only stopping them being *installable
as plugins*.

### 2.2 Make the security plugin hooks-only

`spanner-security` currently contains both the hook and a copy of `spanner-security-standard`. The
skill belongs in the Skills library; the plugin should do one job.

```bash
cd ~/.claude/plugins/marketplaces/spanner && git rm -r plugins/spanner-security/skills
```

> **Before you do this, confirm the skill is live in org settings** (it is, as of 2026-09-18:
> Published, set to Required). If it is not, upload it first — removing it here without that would
> leave the security standard deployed nowhere.

### 2.3 Fix the dead README link

`README.md` refers to `../ROLLOUT.md`, which does not exist. Either write it or remove the sentence.

### 2.4 Commit, PR, merge

```bash
cd ~/.claude/plugins/marketplaces/spanner && git add -A && git commit -m "chore: one plugin, for the hook; skills live in the org library" && git push -u origin HEAD && gh pr create --fill && gh pr merge --squash --delete-branch
```

### 2.5 Remove the retired plugins from org settings

claude.ai → **Organization settings → Plugins** → remove *Spanner project launch*. (*Spanner brand*
went in Part 1.)

---

# 6 · Part 3 — upload the skills to org settings

This is the manual part. There is no API for the claude.ai org Skills library today.

### 3.1 Generate the upload bundle

```bash
cd ~/.claude/plugins/marketplaces/spanner && git checkout main && git pull --ff-only origin main && ./scripts/export-skills-for-org.sh
```

It writes `dist/org-settings/` and prints which skills carry a `references/` subfolder. `dist/` is
gitignored and disposable — regenerate it, never hand-edit it.

```bash
open ~/.claude/plugins/marketplaces/spanner/dist/org-settings
```

### 3.2 Where to go in the UI

claude.ai → click the org name (top-left) → **Organization settings** → under **Libraries & Access**
in the left sidebar → **Skills** → the **Library** tab.

You will see three tabs: **Library** (what is deployed), **Requests** (member submissions awaiting
approval), **Policy** (org-wide rules).

### 3.3 Replace the two wrong ones FIRST

Order matters — these two are costing you accuracy right now.

1. Find **`spanneros-crud-scaffolder`** in the list.
2. Click the **⋮** at the right of its row → **Replace**.
3. Upload `dist/org-settings/spanneros-crud-scaffolder/SKILL.md`.
4. Confirm the description on the row now says **"with NO component library"** and no longer
   mentions shadcn/ui. *If it still says shadcn, the upload did not take — do it again.*
5. Repeat for **`spanneros-schema-migration`**. Confirm the description now mentions
   **"verifies"** and no longer mentions `002_schema_updates.sql`.

> **Use Replace, not Delete-then-Add.** Replace preserves the row's access setting. Deleting loses
> it, and you will not be warned.

### 3.4 Replace the rest of the existing ones

Same **⋮ → Replace** for each of these, to bring them level with the repo:

`apply-project-template` · `project-launch` · `spanner-design-loop` · `spanner-domain-ssl-dns` ·
`spanner-internal-deploy` · `spanner-meeting-notes` · `spanner-operating-model` ·
`spanner-security-standard` · `spanner-weekly-digest` · `spanner-brand-visual` ·
`spanner-brand-voice`

**Three of these have a `references/` subfolder and will lose content if you upload only
`SKILL.md`:**

- `spanner-security-standard` — **the function-grants security rule lives in
  `references/full-standard.md`, not in `SKILL.md`.** Upload the whole folder.
- `apply-project-template`
- `matrix-task-sync`

If the uploader only accepts a single file, zip the skill's folder and upload the zip. If it accepts
neither, upload `SKILL.md` and then **verify by opening the skill in the UI** that the reference
content is present; if it is not, that skill is incomplete and you should say so rather than move on.

### 3.5 Add the three that have never been uploaded

Click **+ Add** at the top right, then upload each of:

`spanner-apps-script` · `torque-design-language` · `matrix-task-sync`

---

# 7 · Part 4 — set the access tier on every skill

Each row has a dropdown on the right. Set them as follows. **This is the step that protects recall
accuracy** — see the README section *How many skills to turn on*.

### Required — on, cannot be disabled (1)

| Skill | Why |
|---|---|
| `spanner-security-standard` | It is a standard. Its value is that nobody has to remember it and nobody can opt out. |

### Installed by default — on, removable (3)

| Skill | Why |
|---|---|
| `spanner-operating-model` | Anyone may be asked how Spanner works. |
| `spanner-brand-voice` | Anyone may write something client-facing. |
| `spanner-brand-visual` | Same, for anything designed. |

### Available to install — visible, off (12)

`apply-project-template` · `matrix-task-sync` · `project-launch` · `spanner-apps-script` ·
`spanner-design-loop` · `spanner-domain-ssl-dns` · `spanner-internal-deploy` ·
`spanner-meeting-notes` · `spanner-weekly-digest` · `spanneros-crud-scaffolder` ·
`spanneros-schema-migration` · `torque-design-language`

**This is not a demotion.** These are real skills used by one or two people. A person switches one
on in a single click, and meanwhile it is not competing for Claude's attention in everyone else's
conversations.

> **If your plan offers per-group targeting**, use it instead for the engineering set
> (`spanneros-*`, `spanner-apps-script`, `torque-design-language`, `spanner-internal-deploy`,
> `spanner-domain-ssl-dns`): default-on for the engineering group, unavailable to everyone else.
> That is strictly better than self-install.

### Not available — use for nothing right now

Reserve it for retiring a skill without deleting it.

---

# 8 · Part 5 — clean up the Mac

### 5.1 The managed settings file

```bash
cat "/Library/Application Support/ClaudeCode/managed-settings.json"
```

It currently enables **both** `spanner-security@spanner` and `spanner-toolkit@spanner`. Since
`spanner-toolkit` is no longer a plugin after Part 2, remove that line. Needs sudo:

```bash
sudo nano "/Library/Application Support/ClaudeCode/managed-settings.json"
```

Leave `spanner-security@spanner` — that is the secret gate, and it should be on everywhere.

### 5.2 Decide whether the secret gate is actually deployed

**This is a real open question, not a formality.** That hook only runs where the managed settings
file exists. It is on Mason's Mac. Whether it is on anyone else's depends on whether they ran
`install-spanner-security.sh`.

Ask, and if the answer is no, either have people run it:

```bash
curl -fsSL https://raw.githubusercontent.com/spanner-product-dev/spanner-claude-marketplace/main/install-spanner-security.sh | sudo bash
```

…or register `spanner-security` in claude.ai → Organization settings → **Plugins** → *Organization
library* and set it to **Required**, which does not need anyone's terminal.

The security standard says *no secrets in code, ever*. A gate that runs on one laptop is not that.

### 5.3 Restart

Fully quit and reopen Claude Code (and the desktop app) so plugin and settings changes load.

---

# 9 · Obsolete files — what to do with each

| Item | Verdict | Action |
|---|---|---|
| `~/Documents/spanner-skills-for-org-settings/` | **Obsolete.** A hand-made export that became a fourth copy. Already deleted 2026-09-18. | If it reappears, delete it. Use `dist/org-settings` instead. |
| `~/.claude/plugins/marketplaces/spanner-plugins/` | **Obsolete after Part 1.** | `rm -rf` the local clone. Keep the GitHub repo dormant as a backup; add a "moved" note to its README. |
| `plugins/spanner-security/skills/` | **Obsolete after Part 2.** | Removed by `git rm`; the skill lives in the org library. |
| `../ROLLOUT.md` (referenced by README) | **Does not exist.** | Write it or drop the reference. |
| `install-spanner-security.sh` | **Keep** — but only if you keep deploying the hook by managed settings. | If you register the plugin in the org library instead (5.2), this becomes obsolete; delete it then and say so in the README. |
| `dist/` | **Disposable by design.** Gitignored. | Delete freely. Regenerate with the script. |
| `~/.claude/plugins/cache/**` | **Never edit. Not a source.** | Leave alone entirely. Overwritten on update. |
| `_staged/` in the screenshot inbox | Unrelated to skills; working copies. | Safe to empty; never move originals into it. |

---

# 10 · The recurring loop — after any skill change, forever

1. Edit the skill **in this repo only**, on a branch.
2. PR → review → merge to `main`.
3. `git checkout main && git pull && ./scripts/export-skills-for-org.sh`
4. In claude.ai org settings → Skills → **⋮ → Replace** on the changed skill(s).
5. Confirm the description on the row changed. **If it did not, the upload did not take.**

**Step 4 is manual and will be forgotten.** That is how `spanneros-crud-scaffolder` spent four
months telling people to use a UI library the project does not have. Put it in the PR checklist.

### The one skill with a source above this repo

`spanner-security-standard` derives from
`SpannerOS/Security Framework/spanner-security-standard.md` in Google Drive, and the skill's own
`references/full-standard.md` says **the Drive document wins on disagreement**. So a security change
is three hops, in this order:

**Drive → this repo → org settings.** Skipping the first makes the Drive copy wrong, and the Drive
copy is the one that is treated as canonical.

---

# 11 · Traps that have already cost time

- **`create or replace` is not the only thing that keys on a name.** Uploading a skill whose
  filename differs from its `name:` frontmatter creates confusion — keep the folder name, the
  `name:` field and the org-settings entry identical.
- **The local marketplace checkout can be behind while the cache is current.** Always `git pull`
  before editing. The cache being right is not evidence the checkout is.
- **Never edit `~/.claude/plugins/cache/`.** It is replaced silently on auto-update.
- **Replace, do not Delete-then-Add**, or you lose the access tier without a warning.
- **`references/` content does not travel with `SKILL.md` alone.** Three skills carry one, and for
  `spanner-security-standard` the reference file holds rules the `SKILL.md` only summarises.
- **A stale skill is worse than a missing one.** A missing skill makes Claude ask. A stale skill
  makes Claude confidently wrong, and nobody checks a confident answer.

---

_Written 2026-09-18, against the state of the org on that date. If the inventory in §2 no longer
matches what you see, trust the screen and update this file._
