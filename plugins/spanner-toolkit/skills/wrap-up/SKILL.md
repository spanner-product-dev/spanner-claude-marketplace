---
name: wrap-up
description: >
  End-of-session wrap-up for any Spanner project. Logs the session to the project's history/ folder,
  updates the plan and notes only if something changed, and tells the user what is unverified and what
  to do first next session. Use when the user says "wrap up", "/wrap-up", "wrap this session",
  "close out this session", "log this session", or is about to end a session that changed files, code
  or a decision. Always invoke it at the end of such a session, even on a short one.
---

# Wrap up the session

This skill does not hold the rules. The Spanner org instructions and the project's own `CLAUDE.md`
define the end-of-session steps, the four-file convention and the size limits. This skill is the
trigger and the checklist. **If the project's `CLAUDE.md` says something different, it wins.** Do not
invent a new structure, and do not copy the rules into a second place where they can drift.

## Before you start

1. **Did this session change files, code or a decision?** If not, say so in one line and log nothing.
2. **Which project?** If you don't already know the project and its Drive folder, ask. Read the
   project's `CLAUDE.md` for its structure and reading list.
3. **If `ClaudeFolders/` or its `portfolio/` folder is missing or empty, stop and tell the user.**
   Never create, restore or rebuild it.

## Do these, in order

1. **`history/session-history.md`** in the project's Drive folder (even if the work was in a code
   repo). One row: `| Date (tool) | Summary |`, directly under the last row, no blank line, newest
   last. Escape any `|` as `\|`. If this session already has a row, edit it to its final state
   instead of adding another. Create `history/` and the file if missing.
2. **`history/YYYY-MM.md`** for the current month. Append a dated section: what changed, what
   shipped, what is unverified. Create the file if the month is new.
3. **`plan-[project].md`**, only if status, priority order or a reference changed. Rewrite Current
   Status as one paragraph. Never stack a dated entry on top of it, and never put a session summary
   in the `Last updated` line. Next Steps stay numbered and prioritized: a title and a few lines.
4. **Decisions.** Add a decision to `notes-[project].md` only if it matters beyond this session, as
   Decision / Why / Implication. Supersede the old one in place instead of appending a correction.
   If the project's `CLAUDE.md` splits notes into an architecture file and modules, follow that.
5. **Open questions** go in the project's open-questions register, naming what they block.
6. **`plan_notes-[project].html`**: rebuild only if the architecture, a major decision or a
   milestone changed, from the plan and notes. Plain md files are the source of truth, so update them first.
7. **Skills.** Look back at the session for work a skill would have made faster or safer:
   - a multi-step procedure you worked out and are likely to repeat (a new skill), or
   - a gotcha, wrong step or missing rule in a skill you used this session (an update to it).

   For each one (usually no more than two), give the skill name, new or update, and what it would
   add. Keep it short, but take the space you need when the change is not obvious. Then offer
   these options and let the user pick:
   - **Write it.** Draft the new skill, or the edited text of the existing one, in its source
     (the spanner-toolkit plugin in `~/Developer/spanner-claude-marketplace`, or wherever the
     skill lives). Use `skill-creator`. Show the change before committing anything.
   - **Update the org skill too.** If the skill is also in the org skill library on claude.ai, make
     the same change there through Claude in Chrome, so Cowork and the desktop/browser app get it.
     Check that the org copy matches the source text after saving.
   - **Not now.**

   Write nothing until the user picks. Skip this step silently if nothing qualifies. A one-off fix,
   or anything that belongs in memory or the project's `CLAUDE.md`, is not a skill.

## Keep it small

- Plan and notes are read every session. Dated narrative goes to `history/`, which is never read at
  session start.
- Split by scope, not by date.
- Code stays out of Google Drive. If this session built code, it lives in `~/Developer` and GitHub;
  only the history and plan files go to Drive.

## Reply

Short. Three things, plus a fourth only if step 7 found one:

1. What you changed (files, one line each).
2. What is still unverified, or what you could not check.
3. The first thing to do next session.
4. Any skill you propose to add or update, with the options from step 7 (write it, also update
   the org skill in Chrome, or not now).

Don't recap the whole session. The history file already has it.
