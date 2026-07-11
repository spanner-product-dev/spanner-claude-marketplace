---
name: spanner-internal-deploy
description: >
  Publish HTML pages to the Spanner internal portal (spanneros-wip.pages.dev).
  Use this skill whenever Mason wants to: deploy a new or updated HTML page to the
  portal, understand how the auto-registration system works, add the right meta tags
  so a page appears correctly in the portal grid, troubleshoot a page that isn't
  showing up, or set up the watcher on a new machine. Also triggers on: "deploy to
  spanner internal", "push this to the portal", "publish this HTML", "add this page
  to the dashboard", "upload to the portal", "how do I get this live", or any
  request to get local HTML pages live at spanneros-wip.pages.dev.
---

# Spanner Internal Deploy

The Spanner internal portal is a Cloudflare Pages site gated by Google SSO
(Cloudflare Access). Only `@spannerpd.com` accounts can view it.

**Live URL:** https://spanneros-wip.pages.dev  
**Upload page (no git required):** https://spanneros-wip.pages.dev/upload.html  
**Repo:** `spanner-product-dev/spanner-internal-website` (branch: `master` = Production)  
**Local path (Mason):** `~/Developer/spanner-internal-website`

---

## How publishing works

```
Drop file into public/
      ↓  (macOS launchd watches the folder, fires after 30 s of quiet)
auto-portal.py runs
  → scans all HTML in public/
  → adds new entries to portal-data.json
  → fixes any broken paths (moved files)
  → git commit + push to master
      ↓  (Cloudflare detects the push, ~30 s build)
spanneros-wip.pages.dev is updated
```

`portal-data.json` is the source of truth for the portal grid. The automation
manages it — never edit it by hand.

A second launchd agent (`com.spanner.autodeploy`, every 5 min) commits modified
pages and, in the same pass, regenerates the grid's **thumbnails** via
`tools/thumbs/gen-thumbs.sh`. The grid shows a pre-rendered WebP image of each
page (not a live iframe), so it stays fast with hundreds of pages. A new or
changed page's thumbnail is captured within ~5 minutes; until then that tile
falls back to a live preview, so nothing looks broken. The step is non-fatal —
if capture ever fails, the content deploy still ships. See
`tools/thumbs/README.md` in the repo for details and manual regeneration.

---

## Publishing a page

### If you have the repo (Mason / admins)

1. Drop an `.html` file anywhere under `public/`
2. Wait ~60 seconds
3. Reload the portal — your page is live and listed in the grid

The launchd watcher handles everything. No git commands needed.

### If you don't have the repo (everyone else)

1. Go to **https://spanneros-wip.pages.dev/upload.html**
2. Drop your `.html` file, pick a section, click Upload
3. Live in ~60 seconds — no git required

---

## Meta tags — control how your page appears in the portal

When you save a file, the portal entry is auto-resolved in this order:

| Field | Resolution order |
|---|---|
| **Title** | `<meta name="spanner-title">` → `<title>` tag (strips trailing " — Spanner") → filename |
| **Section** | `<meta name="spanner-section">` → folder name → `docs` |
| **Status** | `<meta name="spanner-status">` → `reference` |
| **Description** | `<meta name="spanner-description">` → `<meta name="description">` → first `<p>`/`<h2>` text → empty |

To control a page's portal entry explicitly, add any of these to `<head>`:

```html
<meta name="spanner-title"       content="Marketing Tracker">
<meta name="spanner-section"     content="forge">
<meta name="spanner-status"      content="live">
<meta name="spanner-description" content="Tracks active campaigns and channel performance.">
```

### Valid sections

| Value | Portal section |
|---|---|
| `system` | SpannerOS — System |
| `forge` | Forge — BD & Marketing |
| `workbench` | Workbench — Project Delivery |
| `drivetrain` | Drivetrain — Operations |
| `ledger` | Ledger — Finance |
| `brand` | Brand & Infrastructure |
| `trackers` | Project Trackers |
| `presentations` | Shared Presentations |
| `docs` | Internal Docs & Evals |

### Valid statuses

`reference` (default) · `live` · `mockup` · `concept` · `setup` · `paused`

### Folder → section defaults

| Folder | Default section |
|---|---|
| `brand/`, `Website/` | brand |
| `marketing/` | forge |
| `mockups/` | workbench |
| `operations/` | drivetrain |
| `consolidation/` | trackers |
| `claude_tips/`, `docs/` | docs |
| `presentations/` | presentations |
| anything else | docs |

### Files excluded from the portal grid

These deploy fine but won't appear in the grid:
`index.html` · `brand/type-scale-samples/**` · `Website/reference/**` ·
`www.spannerpd.com/**` · `mnt/user-data/**`

---

## Three critical gotchas

**1. Git push to `master` is the only way to update Production.**  
Cloudflare Pages is git-connected: `master` = Production. `wrangler pages deploy`
always creates a Preview deployment (temporary hash URL) when git-connected —
regardless of `--branch` flags. `deploy.sh` is an emergency escape hatch only.

**2. Cloudflare is case-sensitive; your Mac is not.**  
`Website/` (capital W) and `website/` are the same folder on your Mac but
different paths on the live server. Use the exact case that's on disk.

**3. `deploy.sh` is not the normal workflow.**  
The watcher handles everything. Only run `deploy.sh` if git is broken or you
need to push immediately without waiting for the watcher.

---

## Running the script manually

```bash
# Dry run — shows what would change without writing anything
python3 auto-portal.py --dry-run

# Actually run it
python3 auto-portal.py
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Dropped a file, portal not updating after 90 s | Watcher not running, or git push failed | `tail -f /tmp/spanner-portal-watcher.log` — look for Python traceback or git error |
| Watcher not in `launchctl list` | Not installed / got unloaded | `bash install-watcher.sh` from repo root |
| `git push` fails with "private email" error | Git email config | `git config user.email "<github_username>@users.noreply.github.com"` |
| `git push` fails with "unable to read tree" | Corrupted git object (Drive sync issue) | `find .git/objects -size 0 -delete && git fetch origin` |
| File deployed but not in portal grid | In skip list, missing `<title>`, or inside `Website/reference/` | `python3 auto-portal.py --dry-run`; add a `<title>` tag if missing |
| Portal looks stale in Safari | Browser cache | Option+Cmd+E to empty cache, then Cmd+R. Or use Private window (Cmd+Shift+N). Note: Cmd+Shift+R in Safari opens Reader Mode, not force-refresh |
| `portal-data.json` shows broken paths | Files moved between folders | `python3 auto-portal.py` — auto-fixes broken paths via filename lookup |
| Grid thumbnail is blank, stale, or shows a live preview instead of an image | Thumbnail not generated yet (new page, within ~5 min) or capture failed | Wait one autodeploy cycle, or force it: `cd tools/thumbs && node gen-thumbs.mjs --only=<path>` (or `--all`). First run needs `npm install` in `tools/thumbs/`. Check `/tmp/spanner-autodeploy.log` for `thumbs:` lines |

---

## Key paths

| Path | Purpose |
|---|---|
| `~/Developer/spanner-internal-website/public/` | Everything here ships to the live site |
| `public/portal-data.json` | Portal grid data — auto-managed, don't edit |
| `public/thumbs/` | Pre-rendered page thumbnails (WebP) shown in the grid — auto-generated |
| `auto-portal.py` | Auto-registration + deploy script |
| `spanner-autodeploy.sh` | 5-min agent: Drive sync + thumbnail regen + commit/push |
| `tools/thumbs/gen-thumbs.mjs` / `.sh` | Portal thumbnail generator (see its README) |
| `deploy.sh` | Manual wrangler deploy — emergencies only |
| `AUTHORING.md` | Full meta tag reference |
| `/tmp/spanner-portal-watcher.log` | Watcher output log |
| `~/Library/LaunchAgents/com.spanner.portal-watcher.plist` | Installed launchd agent |

---

## Setting up the watcher on a new machine

1. Get repo access — ask Mason to add you as a collaborator on `spanner-product-dev/spanner-internal-website`
2. Clone into your Google Drive share at `_SpannerClaude/ClaudeFolders/<your_name>-Claude/spanner-internal-website/`
3. Set git email: `git config user.email "<github_username>@users.noreply.github.com"`
4. Edit `com.spanner.portal-watcher.plist` — replace Mason's Drive path with yours (two places: `ProgramArguments` and `WatchPaths`)
5. Run once from repo root: `bash install-watcher.sh`
6. Verify: `launchctl list | grep spanner`

---

## Access / SSO context

The site is gated by Cloudflare Access. Any `@spannerpd.com` Google account can log
in — no changes needed when adding new pages. First-time visitors see a Google login
prompt before reaching the site.

If SSO is broken, verify:
- Cloudflare identity provider App ID matches the Spanner Launchlist OAuth client ID (`107337937739-…`)
- Redirect URI `https://snowy-snow-75b2.cloudflareaccess.com/cdn-cgi/access/callback` is in the OAuth client's authorized redirect URIs in Google Cloud
- Google Admin SDK API is enabled in Google Cloud project 107337937739
