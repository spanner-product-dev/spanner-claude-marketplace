---
name: spanner-design-loop
description: >
  Produces a polished, on-brand Spanner visual output through an internal multi-perspective
  design review loop — no raw first drafts handed to the user. Use this skill whenever
  creating any visual deliverable for Spanner: HTML artifacts, reports, dashboards,
  slide decks (PPTX), Word documents (DOCX), SVGs, infographics, email templates, landing
  pages, status pages, or any designed output. Triggers on: "build a branded [anything]
  for Spanner," "create a Spanner [report/deck/page/doc]," "design a [format] for Spanner,"
  "make this on-brand," or any time a visual output needs to follow Spanner brand guidelines.
  The skill runs up to 4 internal design iterations before presenting the final output —
  never show an unreviewed draft. Always use this skill in preference to building visuals
  directly when Spanner brand quality is required.
---

# Spanner Design Loop

You are producing a visual deliverable for Spanner. Before you show anything to the user,
you will run an internal design review loop — simulating three expert reviewers — and
iterate until the output meets the bar all three would accept. Maximum four iterations total.

---

## Step 0: Load Brand References

Before producing anything, read both brand skills in full:

1. **`/spanner-brand-visual`** — complete visual spec: color system, 120%-scale type
   table, accent rules, **logo file library (Step 7)**, **HTML baseline + logo alignment
   (Step 9)**, icon system, compliance checklist
2. **`/spanner-brand-voice`** — voice constants, channel formats, copy rules, validation
   checklist

Pay special attention to Steps 6, 7, and 9 of spanner-brand-visual before placing
any logo. These are your design constitution — every critique tests against them.

---

## Step 1: Understand the Brief

Before building, confirm (from the conversation or by asking once):

- **Output format** — HTML, PPTX, DOCX, SVG, email, infographic, or other?
- **Purpose** — what is this for? Who will read or use it?
- **Content** — what information or data must appear?
- **Background mode** — light (white/light-gray) or dark (Navy)? Default: light.
- **Logo placement** — header, hero, footer, cover page? Note every location.
- **Special constraints** — print dimensions, specific viewport, slide count, etc.

Do not proceed until you can answer all six.

---

## Step 2: Build Draft 1

### 2a — Select and place the logo

Every deliverable includes the Spanner wordmark. Choose the correct file and placement
using the rules below, derived from Steps 6–7 and 9 of spanner-brand-visual.

**File selection by surface:**

| Surface | Logo to use |
|---------|-------------|
| HTML on white/light background | `Spanner-Wordmark-Azure.svg` inline at `height:30px` |
| HTML on Navy / dark section | `Spanner-Wordmark-White.svg` inline at `height:30px`, or the Azure file with `color:#fff` |
| PPTX / DOCX on light | `Spanner-Wordmark-Azure-640.png` (1280px for hero slides) |
| PPTX / DOCX on Navy | `Spanner-Wordmark-White-640.png` |
| Email signature | `Spanner-Wordmark-Azure-320.png` on light; `Spanner-Wordmark-Navy-320.png` as fallback |
| Print | `Spanner-Wordmark-White.eps` or `Spanner-Wordmark-DarkGray.eps` |

All logo files live in `assets/Logo/2026_Spanner_Logo_Files/` relative to the
`spanner-brand-visual` skill, or via the public mirror at
`https://raw.githubusercontent.com/spanner-product-dev/spannerpd-brand-assets/main/brand/Logo/2026_Spanner_Logo_Files/`.
**Use the 2026 set — every file in it is ink-tight.** The older
`0_Spanner Logo Package (External Sharing OK)/` is archival: its 2024 Azure SVG and the
three PNGs rendered from it carry a padded artboard where ink fills only 61.9% of the
declared height, so `height:45px` renders a 27.9px wordmark. Never reference `z_Archive/`,
and never use the legacy Blue files unless matching pre-2024 collateral.

**Inline SVG approach for HTML (preferred over `<img>` for headers and dark sections):**
```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 813.16 170.95"
     style="height:30px;width:auto;color:#fff" aria-label="Spanner">
  <!-- paste the seven paths from 2026_Spanner_Logo_Files/Spanner-Wordmark-Azure.svg -->
  <!-- paths carry fill="currentColor", so `color` on the svg or any ancestor drives it -->
  <!-- dark surfaces: color:#fff  ·  light surfaces: color:var(--navy) or var(--azure) -->
</svg>
```
The viewBox is cropped to the artwork, so **the stated height IS the rendered wordmark**.
Never inline the padded `0 0 965.951 275.986` box.

**HTML header baseline alignment — the s07 lockup:**

`height` spans the full ink, which includes the descender of the **p**. The letter body is
**0.740 × height** and the baseline sits **0.260 × height** above the bottom edge — so a
30px logo gives 22.2px letters. Align the pipe and label to the letter body, not the box:

```css
/* On the flex row containing logo + divider + title: */
.header-inner { display: flex; align-items: flex-end; gap: 24px; }

/* Logo: */
.header-mark  { height: 30px; width: auto; display: block; }

/* Vertical divider bar — spans the letter body, centred on it: */
.header-pipe  { width: 1px; height: 28px; background: var(--azure); margin-bottom: 5px; }

/* Text label next to logo — 22px/400, baseline coincident with the wordmark's: */
.header-label { font-size: 22px; font-weight: 400; line-height: 1; margin-bottom: 5px; }

/* Bar is padding-driven, not fixed-height: */
.header-bar   { padding: 11px 0; }   /* ~60px tall with nav links */
```

These offsets are derived from the cropped geometry. **The older 21 / 14 / 11 values were
tuned against the padded file and are wrong here** — that mismatch is what made previously
correct headers break when the viewBox was cropped.

**Logo clearspace:** height of the lowercase "s" on all sides. Never box, skew, rotate,
add shadow/stroke/opacity, change letter colors, or rearrange characters.

**Minimum size:** 128×29px digital.

### 2b — Build the full output

- Apply the Step 9 HTML baseline CSS block verbatim (HTML outputs)
- Use the 120% type scale from Step 4
- Apply color rules from Step 3
- Apply exactly one accent method from Step 5 (never combine)
- Apply voice constants from Steps 3–4 of spanner-brand-voice
- Apply format-specific rules (sticky header for HTML, master slide for PPTX, etc.)

Format-specific starting points:
- **HTML** — Step 9 baseline CSS; sticky header; logo via inline SVG
- **PPTX** — read pptx skill first; Spanner colors + type scale in theme; PNG logo
- **DOCX** — read docx skill first; Inter, Navy/Azure; PNG logo on cover
- **SVG** — embed Inter via `<defs>`; use brand CSS custom properties
- **Email** — inline styles only; Helvetica Neue fallback; PNG logo; 600px width

Do **not** show this draft to the user.

---

## Step 3: Internal Design Critique

After each draft, score from three reviewer perspectives. Be rigorous.

### Reviewer A — Design Director

Visual craft, brand fidelity, logo compliance, aesthetic quality.

Universal checks:
- [ ] Logo present and using the correct file for this surface and background
- [ ] Logo pulled from `2026_Spanner_Logo_Files/` — not the padded 2024 files, not Archive
- [ ] Logo at correct size (`height:30px` for HTML headers → 22.2px letters; 2026 PNG for PPTX/DOCX)
- [ ] No legacy teal logo (`#49B5CF`) on a surface that uses current Azure `#06A6ED`
- [ ] Logo clearspace respected — no crowding against text or edges
- [ ] Logo not skewed, rotated, shadowed, stroked, or otherwise misused
- [ ] **HTML header alignment is s07**: flex row uses `align-items: flex-end` with `gap:24px`; pipe is `height:28px; margin-bottom:5px`; label is 22px/400 with `margin-bottom:5px`; bar is `padding:11px 0`
- [ ] Inter loaded; 120% type scale applied precisely
- [ ] Navy #293A49 for text (not black or charcoal)
- [ ] White or Navy backgrounds (Light Gray #D4D8DB as neutral only)
- [ ] Azure #06A6ED accents — one method only, never combined
- [ ] No ALL CAPS except abbreviations; section headers lowercase
- [ ] No failing color pairs
- [ ] Generous whitespace; clear visual hierarchy
- [ ] Feels like a premium product studio made it

Format-specific:
- **HTML** — sticky header; no `color:black` or `font-family:Arial` inline
- **PPTX** — consistent margins; no Office default theme remnants;
  `margin: 0` on all text boxes (PowerPoint inset trap); header lockup from the
  2026 PNGs — `lgH = 0.279`, width `lgH * (813.16 / 170.95)`, optical centre at
  **37%** of image height (the padded 2024 files used 0.45 and 45%; do not mix
  a file from one set with the maths from the other, or the wordmark resizes);
  final check rendered in PowerPoint, not only LibreOffice preview
- **DOCX** — named styles used; no Times New Roman
- **SVG** — viewBox set; no hardcoded px on root element
- **Email** — all styles inline; no `<link>` for web fonts; 600px-safe

### Reviewer B — Subject Matter Expert

Content accuracy, completeness, usefulness.

- [ ] All required information from the brief present
- [ ] Information hierarchy matches importance
- [ ] Precise labels — no vague or generic copy
- [ ] Data and facts correctly represented
- [ ] No filler phrases or placeholder text
- [ ] Content clear for the target audience
- [ ] Nothing missing; nothing irrelevant

### Reviewer C — Project Manager

Usability, clarity, goal achievement.

- [ ] Purpose obvious in < 3 seconds
- [ ] Single, specific call to action (if any)
- [ ] Structure fits content volume and format
- [ ] No dead ends in interactive elements
- [ ] Appropriate for the delivery context
- [ ] No unexplained jargon
- [ ] Deliverable achieves its stated goal

---

## Step 4: Critique Summary

After all three reviewers, produce a compact internal summary:

```
ITERATION [N] CRITIQUE
======================
Design Director: [pass / needs work]
  Issues: [bullet list — specific, actionable]

Subject Matter Expert: [pass / needs work]
  Issues: [bullet list]

Project Manager: [pass / needs work]
  Issues: [bullet list]

Overall: PASS / REVISE
```

All three pass → Step 6. Any fail → Step 5.

---

## Step 5: Iterate

Fix every flagged issue. Produce the next draft.

Repeat Steps 3–5 up to **4 iterations total** (Draft 1 = iteration 1).
After iteration 4, proceed to Step 6 regardless. Note unresolved issues in handoff.

Do not show intermediate drafts or critique summaries to the user.

---

## Step 6: Final Output

Present the final file. Follow with a **Design notes** section (3–5 lines max):

1. Logo file chosen and rationale (background mode, surface type)
2. Header alignment approach used
3. Other key brand decisions (accent method, type hierarchy)
4. Any known limitations or trade-offs
5. If iteration 4 hit: list remaining open issues

Format:

---
**Design notes**
[3–5 line prose summary]
[If applicable: Known open issues: ...]
---

Never expose the iteration process or critique summaries. User sees final output + design notes only.

---

## Iteration Budget

| Draft | Action |
|-------|--------|
| 1 | Build per brief + brand spec; select and place logo |
| 2 | Fix Reviewer A/B/C issues — check logo alignment first |
| 3 | Fix remaining issues |
| 4 | Final pass — fix what you can; note what remains |
| → | Present output |

Never exceed 4 iterations. Never show a draft before the loop completes.
