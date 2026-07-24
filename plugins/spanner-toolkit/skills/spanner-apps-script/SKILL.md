---
name: spanner-apps-script
description: Gate and guardrail for every Spanner Google Apps Script change — planner spreadsheets, the ProjectMaster library, master dashboards, exec-summary decks, Harvest sync, the DTO tracker. Use whenever a task involves reading, editing, pushing, or debugging Apps Script / .gs / bound-script code, a Google Sheets planner's macros or named ranges, a custom Sheets menu, or anything under ~/Developer/spanner-apps-script. Triggers on "clasp", "Apps Script", "bound script", "push to the library", "add a menu item", "planner macro", "roll this to the planners", "onOpen", "onEdit", "named range", "Script ID", or any request to change how a planner behaves. Enforces clasp-only (never the web editor, never browser automation), the pull→diff→push→re-pull sequence, and hard-stops with a handoff when the environment can't run clasp. When in doubt, use it — an untracked live edit silently diverges from the repo and has already cost a full recovery session.
---

# Spanner Apps Script — guardrail

Load this before touching any Spanner Apps Script code. It exists because two specific
failure modes have already cost real time, and both are cheap to prevent.

## Step 1 — check the environment before promising anything

| Environment | clasp | OAuth | `script.googleapis.com` | What it may do |
|---|---|---|---|---|
| **Claude Code** (real terminal) | yes | `~/.clasprc.json` | reachable | Everything: pull, diff, push, verify |
| **Cowork** (sandboxed VM) | installable, but useless | none (login is interactive) | **unreachable** | Read the repo, plan, write code into the repo. **Never touch live scripts.** |

Measured in Cowork 2026-07-24: `registry.npmjs.org` → 200, `script.googleapis.com` → 000,
`accounts.google.com` → 000. Installing clasp in Cowork is pointless — it can never
authenticate or reach the API.

Quick check if unsure:

```bash
which clasp; ls ~/.clasprc.json
curl -s -o /dev/null -w "%{http_code}\n" https://script.googleapis.com/v1/projects/x
```

**If clasp can't run: STOP.** Do not proceed, do not improvise. Emit a handoff (Step 5).

## Step 2 — clasp only. No exceptions.

Forbidden, every time, regardless of how reasonable it looks:

- Hand-editing in the Apps Script web editor — untracked, diverges from the repo.
- Browser automation against the Apps Script editor (Claude in Chrome, Control Chrome,
  `execute_javascript`, Playwright). Ruled out by Mason 2026-07-21; standing rule.
- `curl` / `fetch` / `requests` / any language reaching Google APIs to substitute for clasp.
- Installing clasp in a sandbox that can't reach the API, to look like progress.

Reading is not a loophole. If you need to *see* live code, `clasp pull` it or read it from
the git repo. Don't open the editor in a browser to read it.

Why: a **2026-07-14** `clasp push --force` from a stale checkout silently deleted two library
files and removed a menu item from every planner. Google's version history was useless.
And hand-edits are how planners drift — K5 carried a feature the template lacked, and a
blanket template push would have destroyed it.

## Step 3 — the golden sequence

`clasp push` is **whole-project**. It overwrites every file in the target, including files
your local checkout doesn't have.

```
clasp pull        # 1. live HEAD first, always
git diff          # 2. what does live have that you don't? STOP if surprised
<edit>            # 3. smallest possible change
clasp push -f     # 4. push
clasp pull        # 5. re-pull and verify HEAD
```

Step 5 is mandatory. "Pushed successfully" is not verification.

**Concurrent sessions:** multiple chats have edited this repo at once and one reverted
another's work (2026-07-20). Pull immediately before pushing. The ProjectMaster library is
**single-writer**.

## Step 4 — fleet rollouts are surgical

Live planners are not template copies; each has accumulated features. Per planner:
pull → diff → patch only the changed block → push → verify. Never push template contents
into a planner.

Test destructive changes on the sandbox first: `sandbox-feno`
(`1nI1B_iV9N385nycm_IEwM3eVMNCEY8JxCbCF77_100eGOsY6puG0kg5k`) or sandbox planner
`1bXw3P7i5hRw7alJZPKkr81YHm4-KGo71MVKJceiN_TY`.

## Step 5 — the handoff, when blocked

Don't just refuse. Write a brief the next session can execute without re-deriving anything:

1. What must be pulled (directory + Script ID, or "Script ID unknown — capture from
   Extensions → Apps Script → Project Settings").
2. What to read once pulled, and the specific questions it answers.
3. Proposed design, with the open decisions called out as decisions.
4. Test plan, sandbox first.

Save it as a dated `.md` in the project folder and say plainly that the work continues in
Claude Code.

## Sheet geometry rules

Address the grid through **named ranges**, never hardcoded A1. Planners span multiple
template vintages; older ones lack newer ranges. Use the candidate-list + Script-Property
A1 override pattern from `dto-tracker/DTOForecastSync.js` (`DTO_RANGE_*`).

Gotchas that have each caused a bug:

- It is **`ratesNames`**, not `rateNames`.
- It is **`BDCheck`**, not `BD` (`Named range "BD" does not exist` was a live failure).
- `HEADER_ROW = 28` on Sheet1 is the week-number row; locate columns by scanning it,
  not by assuming a fixed column.
- Column grouping must respect **both** BD gates: `BDCheck` checked, or `HarvestID`
  starting with `"BD"`.

**Reuse, don't rewrite:** `planner-template/macros.js` → `UseSTUBSonEdit` contains
`shiftFormulaColRefs_(formula, offset)`, which shifts relative A1 column references by an
offset and correctly leaves `$`-absolute refs alone. Any column-shifting feature should
use it.

## Bound-script conventions

- A custom-menu callback string resolves against the **planner's own bound script**, never
  the library. Every menu item needs a local passthrough stub:
  `function foo(){ _maybeRenameScript_(); ProjectMaster.foo(); }`
- Adding a feature to the library makes the menu item *appear* fleet-wide but only *work*
  where the stub exists. Library side is half the job.
- `if(false)GmailApp.getAliases();` and similar are deliberate static-scope-analysis hints
  that force OAuth scope propagation. Do not remove them as dead code.
- After adding scopes, the first run may need a second click — the granting run's token
  still reflects pre-grant scopes.
- Consumers bind ProjectMaster in `developmentMode` (HEAD), so a library push is live
  immediately, with no version to cut — and no safety net either.

## Secrets

None in the repo; use Script Properties. **Known unfixed violation:**
`harvest-api-connector-copy/HarvestApiSync.js` has a hardcoded Harvest PAT (`HC_TOKEN`)
committed to GitHub — rotate and move it. Never copy that pattern.

## Where things live

Repo: `~/Developer/spanner-apps-script` (GitHub `spanner-product-dev/spanner-apps-script`).
Full Script ID registry, live-planner table, and named-range inventory: that repo's
`CLAUDE.md`. Plans and decision log: `plan.md` / `notes.md` in the Drive folder
`_SpannerClaude/.../Existing Spanner Planners/`.

Never put code, `node_modules`, or build output in a Google Drive–synced folder.
`.md`, `.sql`, `.html` docs are fine there.

## Known gap worth closing opportunistically

Most **live client planners are not clasp-tracked** — spreadsheet IDs are known, bound
script IDs mostly are not. This blocks work repeatedly. Whenever you have clasp auth and a
planner open, capture its Script ID (Extensions → Apps Script → Project Settings), add
`planners/<slug>/.clasp.json`, and `clasp pull` it into the repo. Then Cowork sessions can
read real live code without needing clasp at all.
