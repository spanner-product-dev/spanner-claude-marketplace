---
name: apply-project-template
description: Applies the Spanner new-project template to the current project folder — copies the standard files (CLAUDE.md, plan/notes, security-checklist.md, _README.md, _gitignore, _env.example), merges template content into files that already exist without overwriting project content, and fills every [bracket] placeholder with real values found in the project. Use whenever Mason asks to "apply the template", "set up this project", "add the standard project files", "bring this project up to standard", "initialize project docs", "backfill CLAUDE.md / the security checklist", "fill in the placeholders", "run the new-project setup", or starts work in a project folder that's missing CLAUDE.md, plan/notes files, or a security checklist. Also use when a project's template files still contain [PROJECT NAME]-style placeholders that need filling. When in doubt, use this skill — a project missing its standard files drifts from the security standard fast.
---

# Apply Project Template

Bring any Spanner project folder up to the standard structure: the template files exist, nothing the team already wrote is lost, and every `[placeholder]` is replaced with real project information.

## Template source

Primary: `…/Shared drives/_SpannerClaude/ClaudeFolders/Shared-Claude/_new-project-template/`
Fallback: `…/Shared drives/_SpannerClaude/ClaudeFolders/Mason-Claude/Projects/_new-project-template/`

If neither path is readable from this session, ask the user to connect the folder (folder-access request) rather than reconstructing the template from memory — the template is versioned and memory will drift from it.

Template contents (verify with `ls` — the template may gain files over time, and any new file should be handled by the same rules):

| File | Becomes | Notes |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md` | Session context + security rules |
| `plan-PROJECTNAME.md` | `plan-<shortname>.md` | Living plan (source of truth) |
| `notes-PROJECTNAME.md` | `notes-<shortname>.md` | Decision log (source of truth) |
| `security-checklist.md` | `security-checklist.md` | Compliance status + deviations |
| `_README.md` | `_README.md` | Repo README staging copy |
| `_gitignore` | `_gitignore` | Repo .gitignore staging copy |
| `_env.example` | `_env.example` | Repo .env.example staging copy |
| `HOW-TO-USE.md` | **do not copy** | Instructions for the template itself — they don't belong in a real project |

## Workflow

### Step 1 — Identify the project and gather facts FIRST

Do not write anything until you know what's true about this project. Placeholders filled with guesses are worse than placeholders left blank — they look authoritative and get trusted.

1. **Project name + short name.** The folder name is the project name. The short name comes from existing `plan-<shortname>.md` / `notes-<shortname>.md` files if present; otherwise derive a lowercase slug from the folder name and confirm it with the user (offer "leave blank" too, per the org convention).
2. **Mine the folder for facts.** Read any existing `CLAUDE.md`, `plan-*.md`, `notes-*.md`, README, and grep the folder (including HTML/SQL files) for: Supabase project ref (`grep -roE '[a-z]{20}\.supabase\.co'`), GitHub repo (`spanner-product-dev/...`), deployed URL (`*.pages.dev`), DRI name/email, tech stack signals (package.json → Next.js; standalone `.html` files calling Supabase REST → self-contained HTML app), and security posture (RLS mentions, documented deviations like OD-numbered items).
3. **Build a facts table** — every placeholder in the template mapped to either a found value (with where you found it) or "unknown". Read `references/placeholder-map.md` (in this skill's own directory, next to SKILL.md — not in the project or template folder) for the full list of placeholders and where each value usually lives. If you can't locate it, derive the list by grepping the template files for `\[`.
4. Anything still unknown after mining: ask the user in one batch (don't drip questions), or fill with a visible `TODO:` marker and list it in the final report. Never invent a value.

### Step 2 — Copy, rename, or merge each file

For each template file, exactly one of three cases applies:

**A. File doesn't exist in the project → copy + rename + fill.**
Copy it in, rename `PROJECTNAME` files to the short name, fill placeholders from the facts table. In `CLAUDE.md`, delete the "replace every [PLACEHOLDER]" instruction block once filling is done — its presence is the template's "not yet set up" flag.

**B. File exists but is still mostly template** (contains `[PROJECT NAME]` or other bracket placeholders) **→ fill in place.**
Treat it as an unfinished copy of the template: replace the placeholders, keep any real content someone already added.

**C. File exists with real project content → merge, never overwrite.**
The project's content always wins. Compare section-by-section against the template and add only what's missing:
- A template section absent from the existing file → append it (filled, not with raw placeholders).
- A section present in both → leave the existing one alone, even if it's structured differently than the template. Don't "normalize" the team's writing.
- Never duplicate a section, never delete or reword existing content, never reorder what's there.
- For `_gitignore`: union of lines (add template patterns the existing file lacks; keep everything already there).

If a merge decision is genuinely ambiguous (e.g., the existing file covers the same ground under different headings), show the user the proposed additions before writing rather than guessing.

### Step 3 — Make the boilerplate true

The template's prose assumes a default stack (Next.js + npm + `.env.local`). Filling placeholders isn't enough if the surrounding text is false for this project:

- **Tech stack tables / local-dev sections** in `_README.md` and `CLAUDE.md`: rewrite to the project's actual stack discovered in Step 1. A planning folder of self-contained HTML files should not ship a README telling people to run `npm install`.
- **`_env.example`**: if the project has no server-side code and no env vars (anon-key-in-HTML pattern), rewrite it to say so explicitly and why that's safe (RLS + Cloudflare Access), keeping the never-commit-keys and revoke-and-rotate rules.
- **`security-checklist.md`**: check the boxes that are actually true (verify, don't assume — e.g., confirm Layer 2/3 applicability from what data the project handles), mark N/A layers with the reason, and carry any documented deviations found in notes/plan into the Deviations table with their existing IDs (OD7, OD8, …) — don't renumber them.

### Step 4 — Verify and report

1. Grep the touched files for remaining brackets: `grep -nE '\[(PROJECT|PLACEHOLDER|DATE|project-id|repo-name|app-name|folder-id|Name)' <files>` — anything left should be an intentional `TODO:` you're about to report, not an oversight.
2. Log the work in the project's plan file (Complete section) and notes file (Session History) per the org convention.
3. Report to the user: a table of files **created / filled / merged / skipped**, what was added in each merge, and the list of remaining TODOs with what's needed to resolve each.

## Things that have gone wrong before (avoid these)

- **Filling placeholders before mining the project** → plausible-looking wrong values (a Supabase ref from a *different* project found in a shared snippet, for example). Always note *where* each fact came from.
- **Overwriting a real plan/notes file with the template skeleton.** These files are the project's source of truth; merging means the template adapts to them, never the reverse.
- **Copying `HOW-TO-USE.md` into the project.** It documents the template, not the project.
- **Leaving the Next.js boilerplate in a non-Next.js project.** False documentation is worse than no documentation.
- **Google Drive paths differ between file tools and the shell.** In Cowork, Read/Write/Edit use the host path while bash uses the session mount — translate before shelling out, and prefer the file tools for edits.
