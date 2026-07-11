# Placeholder Map

Every `[bracket]` placeholder across the template files, and where its real value usually lives. Build the facts table from this before writing anything.

## Identity

| Placeholder | Where to find the value |
|---|---|
| `[PROJECT NAME]` | The project folder name. Appears in CLAUDE.md, plan, notes, security-checklist, _README, _env.example titles. |
| `PROJECTNAME` (in filenames) | Short slug from existing `plan-*.md` / `notes-*.md` filenames; else slugified folder name, confirmed with user. |
| `[Name, email]` (DRI) | Existing CLAUDE.md/plan; the user's email from session context; else ask. |
| `[Name or internal]` (client/stakeholder) | Plan/notes mentions of a client; internal tools say "Internal (Spanner PD team)". |
| `[One sentence — what problem does this solve?]` | Plan's Current Status paragraph; else ask — one sentence, not a paragraph. |
| `[Planning / Build / Live]` | Plan's Current Status: deployed URL mentioned → Live; migrations applied but not deployed → Build; else Planning. |

## Tech + infrastructure

| Placeholder | Where to find the value |
|---|---|
| `[e.g., Next.js + Supabase · Cloudflare Pages · TypeScript]` | `package.json` present → read its deps. Standalone `.html` files with `supabase.co` fetch calls → "Self-contained HTML + vanilla JS · Supabase REST (anon key, RLS) · Cloudflare Pages". |
| `[project-id]` (Supabase) | `grep -rhoE '[a-z]{20}\.supabase\.co' *.html *.md *.sql \| sort -u` — if more than one ref turns up, ask which belongs to this project. |
| `[repo-name]` (GitHub) | Existing docs, deploy manifest entries, or notes. Org is always `spanner-product-dev`. |
| `[app-name].pages.dev` | `grep -rhoE '[a-z0-9-]+\.pages\.dev' \| sort -u`. |
| `[folder-id]` (Drive) | Rarely needed; omit the row or mark TODO unless the user has it handy. |
| `[Layer 1 / Layer 2 / Layer 3]` (_env.example header) | Match the layers checked in security-checklist.md. |

## Security checklist specifics

| Item | How to resolve |
|---|---|
| Layer 1 checkbox | Always applies if the project stores any person-related data (names, Slack IDs, dates). State *what* data makes it apply. |
| Layer 2 / Layer 3 checkboxes | Only if enterprise customers / regulated data are real. Internal tools: leave unchecked with "N/A — internal tool" / "N/A — no payments, financial, or health data". |
| Deviations table (`OD1 \| \| \| \|`) | Search notes/plan for existing OD-numbered deviations and copy them in verbatim with their original IDs. Replace the empty OD1 row. If none exist, leave the empty row. |
| Sign-off table | Leave unchecked — the user signs off, not the skill. |

## Plan / notes templates

| Placeholder | How to resolve |
|---|---|
| `[DATE]` | Today's date, ISO format. |
| `[session N — one-line summary]` | If creating fresh: "session 1 — project initialized, template applied". If merging: don't touch the existing line. |
| Current Status / Complete / In Progress / Next Steps bodies | Fresh file: write a real first entry from what's known ("Template applied <date>; next: <first concrete step>"), not the bracketed prompts. Merging: leave existing sections untouched. |
| Architecture/Schema Decision stubs (notes) | Fresh file: keep the commented examples as-is — they're prompts for future entries, not placeholders to fill. |
| Open Questions stub | Fresh file: keep as-is, or seed with real open questions surfaced during fact-mining (unknown Supabase ref, unconfirmed repo, etc.). |

## Rule of last resort

A placeholder you cannot resolve becomes a single visible line: `TODO: <what's needed and who can provide it>` — and it goes in the final report. Never leave a raw `[bracket]` behind, and never fill one with a guess.
