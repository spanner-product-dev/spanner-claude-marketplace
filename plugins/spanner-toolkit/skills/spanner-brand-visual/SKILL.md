---
name: spanner-brand-visual
description: >
  Applies Spanner's visual brand guidelines to any output — HTML artifacts, presentations,
  documents, reports, dashboards, SVGs, or any designed deliverable. Use this skill whenever
  creating or styling visual content for Spanner: "make this on-brand", "apply Spanner
  styles", "use our brand colors", "style this for Spanner", "build a branded HTML page",
  "create a Spanner-styled report", "apply our visual identity", or any time an HTML, PPTX,
  DOCX, SVG, or infographic is being created in the Spanner Brand workspace. Also triggers
  when reviewing existing content for visual brand compliance — "does this look on-brand?",
  "check our brand colors", "is this using the right font?". When in doubt, apply this skill —
  catching an off-brand visual is far better than delivering one.
---

# Spanner Brand Visual

You're applying or reviewing the visual identity of Spanner, Inc. — a premier Silicon Valley
product development studio. Spanner has a precise visual system: Navy and White as the primary
pair, Inter as the only font, Azure as the primary accent, and a carefully controlled emphasis
system. Your job is to make outputs that look unmistakably Spanner.

## Step 0: How to use this skill (read first)

Treat conformance as a **measured, top-down audit — not a "fix what looks off" pass.**
When asked to make something on-brand, build a branded deliverable, or conform to this skill:

1. **Audit the whole surface, most-prominent element first.** The header/logo lockup is
   usually the first thing on the page — never skip it. Walk every item in the Step 10
   checklist and every numeric value in this skill (type scale, logo size, pipe spacing,
   alignment offsets) one by one.
2. **Measure the rendered output against the spec's numbers — don't eyeball, and don't
   trust the source value alone.** In a browser, read computed styles and element geometry
   (`getBoundingClientRect`); for SVG logos measure the actual letterform bounds
   (`getBBox`), because an element's bounding box is not the same as its visible glyphs.
3. **Produce an explicit pass/fail report before declaring it done**, so every gap surfaces
   at once instead of being discovered one at a time.
4. **Re-verify after every change** — a fix can introduce a regression. "Looks branded" and
   "the boxes line up" are not the same as "matches the spec."

Do not assume a pre-existing brand CSS block, template, or logo lockup is already compliant —
verify it against the numbers below.

## Step 1: Use This Skill as the Visual Reference

This skill is self-contained — the complete visual specification is embedded in the steps
below. No external files are required. Cover all steps before making any styling decisions;
the details matter (e.g., the exact highlight-effect baseline, icon creation grid, minimum
logo size).

If a `branding.md` file is present in the workspace, you may read it for additional context,
but it is not required — this skill takes precedence for all visual decisions.

## Step 2: Identify the Output Type

Different surfaces need different treatments. Before styling anything, establish:

- **Output format** — HTML artifact, PPTX slide deck, DOCX document, SVG, email template,
  dashboard, infographic, or other
- **Background mode** — light (white/light gray) or dark (Navy)
- **Accent need** — does this surface call for emphasis? Which accent method fits?
  (Choose exactly one: Azure text, bold, or highlight effect — never combine.)
- **Icon need** — are icons needed? Which style?

## Step 3: Apply the Color System

### Primary pair
- Navy #293A49 as background → always pair with White #FFFFFF text
- White #FFFFFF as background → use Navy #293A49 for text (never black or charcoal)
- For body/content surfaces, when in doubt: white background, navy text, azure accent

### Header standard (default)
- The header band of any branded deliverable — HTML page, report, dashboard, slide title bar, email template — **defaults to a Navy #293A49 background with the white wordmark**.
- White-on-dark is also the **default logo lockup** everywhere; reach for the white wordmark first.
- An **Azure wordmark on a light header is the exception**, used only with a deliberate reason (predominantly light/print piece, or matching an existing light surface) — never as an unconsidered fallback. A light header with the Azure logo is off-standard by default.
- Content below the header may still be light; only the header band defaults dark.

### Accent colors
- Azure #06A6ED — primary accent: pipe delimiters, tagline, Azure text accent, highlight borders. Use first.
- Orange #E2672A — secondary: use only when Azure is already present, or to annotate visuals
- Light Blue #CAECF6 — supporting: highlight-effect background, tint backgrounds
- Light Gray #D4D8DB — supporting: dividers, neutral backgrounds

### Color rules
- **No green of any shade** except #0C7C59 for sustainability content (reserved, do not use currently). Common hallucinated greens — #256E30, #4CAF50, #2E7D32, any #A5D6A7-range or teal-green — are off-brand. Replace all "good/positive" indicators (badges, availability states, price savings, status dots) with Azure #06A6ED or Light Blue #CAECF6.
- **Data-series exception (ratified 2026-06-09, internal data surfaces only):** charts, capacity grids, and dashboards may use the 14-color extended data palette — azure #06A6ED, orange #E2672A, green #1E7D4F, violet #6A5FA8, amber #D9A514, deep azure #04679C, berry #B23A6F, olive #6F7D2F, slate #5E7287, sienna #9C4A14, plum #8D4A86, navy #293A49, dusty rose #C77E8E, gray #97A2AC — including the two greens. Family ramps: Tin client owns the blues (sky #6FC6F2 → azure → steel #2E7FAD → deep #04679C → midnight #073D5C); the gray ramp (silver #B9C1C8 / gray #97A2AC / steel #76828D / charcoal #55606B) is reserved for internal/NB/time-off buckets. Red #D94040 stays alerts-only; sustainability green #0C7C59 stays reserved; marketing/client-facing surfaces stay strict-brand. Reference: `SpannerOS/mockups/spanner-data-palette.html`.
- **Azure #06A6ED is the only approved blue.** Do not introduce any other blue value (e.g. #49B5CF legacy, #0070A8, #0066CC, or approximations). If in doubt, use `var(--azure)` or the hex directly.
- Failing pairs (never use): Azure on Green, Green on Azure, Orange on Azure,
  Azure on Orange, Orange on Green
- Passing pairs: White/Navy (AAA), Orange/Navy (AAA), Azure/Navy (AAA), Azure/White (AA only)
- No teal — replace any legacy teal references

## Step 4: Apply Typography

Only font: Inter (Google Fonts: https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap)
Fallback: "Helvetica Neue", Helvetica, sans-serif

| Role | Style | px (size / line-height) | pt (size / line-height) |
|------|-------|------------------------|------------------------|
| Primary headline (1 per page) | Inter Regular | 66.67 / 77.33 | 50 / 58 |
| Subhead | Inter Regular | 38.67 / 48 | 29 / 36 |
| Minor subhead / big subtitle | Inter Regular | 29.33 / 38.67 | 22 / 29 |
| Overline, labels | Inter Bold | 14.67 / 18.67 | 11 / 14 |
| Captions, fine print | Inter Italic | 17.33 / 22.67 | 13 / 17 |
| Body Big (first sentence emphasis) | Inter Regular | 18.67 / 29.33 | 14 / 22 |
| Body standard | Inter Regular | 17.33 / 25.33 | 13 / 19 |
| Body emphasized | Inter Bold | 17.33 / 25.33 | 13 / 19 |
| Body small | Inter Regular | 14.67 / 18.67 | 11 / 14 |
| Body small emphasized | Inter Bold | 14.67 / 18.67 | 11 / 14 |
| Micro / table fine print | Inter Regular | 12 / 16 | 9 / 12 |

**Micro tier (added 2026-06-22).** The smallest sanctioned size — 12px / 16px — for
table sub-labels, price/duration notes, table footnotes, and reference fine print where the
14.67px body-small tier is too heavy for dense layouts. Use sparingly; it is not a substitute
for body copy.
- **Color & contrast — two tiers.**
  - *Must-read micro text* (table values, data, required notes): clear AA (≥ 4.5:1) — Navy
    `#293A49` or no lighter than `#65717C` (≈ 5:1 on white). On Navy, white at ≥ 0.75 opacity.
  - *De-emphasized helper hints* (input/section hints, footnotes, the small caption under a
    label — e.g. "rollup from B2 role matrix…"): **`#949DA4`** (Navy at ~50%) is the approved
    quiet-hint gray — a deliberately recessive, sub-AA treatment for genuinely optional helper
    text (as on the EFM v2.0 page). Do not use it for anything a user must read.
  Use full-opacity hexes rather than dimming Navy with `opacity` (opacity inherits and is easy
  to mis-measure — a navy span at `opacity:0.42` renders ≈ `#A5ACB3`).
- Regular weight, not italic — this is the approved non-italic small tier. The italic
  Captions/fine-print row above remains for editorial captions; use this micro tier for
  functional UI fine print (tables, notes, footers).

Print copy-dense: Headline Inter Bold 19pt, Subhead Inter Bold 14pt,
Body Inter Regular 10pt, Caption Inter Italic 7pt.

Case rules:
- Never ALL CAPS (only abbreviations/acronyms)
- **`text-transform: uppercase` is banned in CSS** — this violates the no-ALL-CAPS rule even when the HTML source text is already lowercase. Scan every CSS rule for this property and remove it.
- Section titles and deck subheads: lowercase
- Sentence case: initial cap only ("We are a creative product development team")

## Step 5: Type Accents

Pick exactly one per surface. Never combine.

Azure Text Accent:
- Up to 4 words → set to #06A6ED
- Keep on same line when possible
- Do NOT combine with highlight effect

Bold Accent:
- Up to 4 words → bold weight
- Best when single color only is available
- Do NOT combine with highlight effect

Highlight Effect:
- #CAECF6 background behind text
- Height = character height; baseline at bottom edge of "e"
- ~1 thin space (U+2009) padding each side
- Can span lines; works on headers and body
- Do NOT combine with Azure text accent

Pipe Delimiters:
- Color: Azure #06A6ED — on both light and dark (Navy) backgrounds. Do not use `rgba(255,255,255,.25)` or other white-tinted variants on dark backgrounds; Azure-on-Navy is AAA and is the intentional look.
- **3 spaces each side, in every context** — body copy, email signatures, and inline lockups (unified 2026-06-28; was 2 spaces for body copy / 3 for signatures).
- In HTML/flex layouts the pipe is an element, not a character: set ~3 space-widths at the surrounding text size (≈15px each side at 17.33px Inter), and **measure the gap to the visible glyphs, not the element boxes** — crop the logo viewBox to the letterforms (Step 9) so box edges equal glyph edges, then confirm left/right gaps are equal by measuring.
- The calibrated **s07 header lockup** (Step 9) carries its own ratified gap; keep s07's value there unless the whole lockup is re-proportioned.
- Example: product strategy   |   industrial design   |   www.spannerpd.com

## Step 6: Logo & Favicon

Wordmark: lowercase "spanner" only (Yaro Rg modified)
Clearspace: height of lowercase "s" on all sides
Minimum: 128×29px digital / 1×0.2578 inch print
Tagline use: rare — "what's next" in Azure, offset from wordmark

Favicon/avatar: White S on Azure circle; S covers ≥50% interior; ≥15% border padding;
15% clearspace around outer shape

Logo misuse — never: skew, rotate, add opacity/shadow/stroke, box in shape,
change letter colors, make fully Azure, rearrange characters.

Letterform metrics for alignment math. **Since the 2026 file set (2026-09-11) every
approved asset uses one geometry** — ink-tight, aspect `813.16 / 170.95 = 4.757`:
- **Cropped geometry (everything in `2026_Spanner_Logo_Files/`, and the inline snippets):**
  letters run from the top edge to **74%** of height (the baseline), descender to the bottom
  edge; x-band optical center at **37%** of height. This now applies to the PNG and SVG files
  alike, so PPTX/DOCX/email placements and inline HTML share one set of numbers.
- **Padded legacy geometry** (`0_Spanner Logo Package…/2024_Azure_Refresh/` SVG + its three
  PNG renders, canvas `0 0 965.951 275.986`, aspect 3.500): visible strokes occupy ~22%–68%
  of file height, optical center at 45%. **Only** for decks and documents already built
  against those files — do not use for new work.

## Step 7: Logo File Library

All Spanner logo files live in the workspace at https://raw.githubusercontent.com/spanner-product-dev/spannerpd-brand-assets/main/brand/Logo.

**Reach for `2026_Spanner_Logo_Files/` first — it is the current set and covers every case.**
One flat folder, correct geometry in every file: ink-tight viewBox, no intrinsic width/height
on the SVGs, colour through `currentColor`, and PNGs re-rendered so 320 px of image is 320 px
of wordmark. Its `README.md` carries the full rationale.

`0_Spanner Logo Package (External Sharing OK)/` is retained for archival and for matching
pre-2026 collateral; its 2024 Azure SVG and the three PNGs rendered from it carry a padded
artboard (see the metrics note in Step 6). Use `2_Export Logo Files/` for additional internal
exports, `1_Native Logo Files/` only when handing source files (.ai, .psd) to a designer, and
never anything from `z_Archive/`.

`Spanner-Color-Palette.png` in the older package is a **deprecated 2015 palette** — measured
swatches are a legacy blue plus coral, purple, yellow and lime, none of them current brand.
Never cite it; `branding.md` is the authoritative palette.

### Current set — `2026_Spanner_Logo_Files/`

| File | Format | Best for |
|---|---|---|
| `Spanner-Wordmark-Azure.svg` | SVG, vector | **Inline HTML, web, anything CSS-sized.** Default Azure `#06A6ED`; inherits `color` when inlined |
| `Spanner-Wordmark-White.svg` | SVG, vector | White default — `<img>` on dark, or where inheritance is inconvenient |
| `Spanner-Wordmark-Navy.svg` | SVG, vector | Navy `#293A49` default — formal documents, single-colour work |
| `Spanner-Wordmark-{Azure,White,Navy}-320.png` | PNG, transparent | Email signatures, small web placements |
| `Spanner-Wordmark-{Azure,White,Navy}-640.png` | PNG, transparent | Standard web/slide placements |
| `Spanner-Wordmark-{Azure,White,Navy}-1280.png` | PNG, transparent | Hero placements, retina, large slides |
| `Spanner-Wordmark-White.eps` | EPS, vector | Print on Navy or dark photographic backgrounds |
| `Spanner-Wordmark-DarkGray.eps` | EPS, vector | Print, single-colour reproduction |
| `Spanner-Wordmark-Blue-Legacy2015.eps` | EPS, vector | Legacy `#49B5CF` — the only EPS in a brand colour until a designer re-exports an Azure one. Not for new work |

### Legacy package (`0_Spanner Logo Package (External Sharing OK)`)

**Archival — prefer `2026_Spanner_Logo_Files/` above for all new work.** These entries are
kept so existing decks and documents can be matched and maintained. The 2024 Azure SVG below
is still the authoritative *source* geometry; it is its padded artboard, not its artwork, that
the 2026 set corrects.

| File | Format | Best for |
|---|---|---|
| `2024_Azure_Refresh/Spanner_Logo_Azure_2024.svg` | SVG, vector | Authoritative source geometry. **Padded artboard — do not place inline;** use `Spanner-Wordmark-Azure.svg` |
| `2024_Azure_Refresh/Spanner_Logo_Azure_2024_320px.png` | PNG, transparent | Padded render (ink fills 62% of height) — superseded by `Spanner-Wordmark-Azure-320.png` |
| `2024_Azure_Refresh/Spanner_Logo_Azure_2024_640px.png` | PNG, transparent | Padded render — superseded by `Spanner-Wordmark-Azure-640.png` |
| `2024_Azure_Refresh/Spanner_Logo_Azure_2024_1280px.png` | PNG, transparent | Padded render — superseded by `Spanner-Wordmark-Azure-1280.png` |

Color-neutral and dark-mode files (always safe — no legacy color):

| File | Format | Best for |
|---|---|---|
| `150810_Spanner_Logo_White-only.svg` | SVG, vector | Correctly cropped 2015 export — the model the 2026 set follows. Superseded by `Spanner-Wordmark-White.svg` |
| `150810_Spanner_Logo_White-only.eps` | EPS, vector | Print on Navy or dark photographic backgrounds |
| `Spanner-Logo-White-Rev-01.png` | PNG, transparent | Dark backgrounds, web/email at fixed size |
| `Spanner-Logo-Dark-Gray-Rev-01.png` | PNG, transparent | Light backgrounds where Blue is too loud (formal docs) |
| `Spanner-Logo-Dark-Gray-Rev-01.eps` | EPS, vector | Print, single-color reproduction |

Legacy 2015 Blue files — still officially approved, but use only when:
(a) you need EPS for print and the 2024 SVG can't be used, or
(b) you're matching pre-2024 collateral still in circulation.

| File | Format | Notes |
|---|---|---|
| `Spanner-Logo-Blue-Rev-01.png` | PNG | Legacy `#49B5CF` |
| `Spanner_Logo_Blue.eps` | EPS | Legacy `#49B5CF` — use until designer re-exports a 2024-Azure EPS |
| `Spanner-Logo-Rectangle-Blue-Rev-01.png` | PNG | Legacy Blue avatar tile |
| `Spanner-Logo-Rectangle-Dark-Gray-Rev-01.png` | PNG | Dark Gray avatar tile (color-safe) |
| `Spanner-Logo-Square-Blue-Rev-01.png` | PNG | Legacy Blue square avatar |
| `Spanner-Logo-Square-Dark-Gray-Rev-01.png` | PNG | Dark Gray square avatar (color-safe) |

### Additional exports (`2_Export Logo Files/`)

| File | Notes |
|---|---|
| `Spanner_Logo_Blue.svg` | Vector blue wordmark — **see color caveat below** |
| `200103_Spanner_Logo_Light_Gray.png` / `.eps` | For very subtle/watermark applications |
| `221201_Spanner_Logo_Black.png` | Pure black — only for QR codes or strict mono printing |
| `Logos for QR Codes/` | Pre-sized variants for embedding inside QR code centers |
| `Spanner-Logo-White-on-Blue_Rev-01.png` | Composite: white logo on solid blue panel — use sparingly |

### How to choose

White-on-dark is the default lockup (see Step 3 Header standard). Reach for the white wordmark on a Navy header first; the Azure-on-light rows below are the documented exception.

- **Header band (default, any format)** → Navy #293A49 band + white wordmark. In HTML, embed the inline snippet below (cropped viewBox) at **`height:30px`** with `fill:#fff` (or `fill:currentColor` on a navy element) — the s07 standard lockup (Step 9).
- **HTML artifacts with dark sections** → embed the inline snippet at **`height:30px`** (scale up proportionally for hero placements); swap `fill:#fff` to `fill:currentColor` so it adapts to the surface
- **PPTX / DOCX on Navy** → use `Spanner-Logo-White-Rev-01.png`
- *(Exception)* **HTML artifacts on white** → only when a light header is the deliberate choice, embed the Azure inline snippet (cropped viewBox) at **`height:30px`**, or use the matching PNG via `<img>` sized so the visible letters match ~22px
- *(Exception)* **PPTX / DOCX on light backgrounds** → `Spanner_Logo_Azure_2024_640px.png` (or 1280 for hero slides)
- **Print** → SVG (current Azure) or legacy Blue EPS until a 2024-Azure EPS is re-exported by a designer
- **Email signature** → `Spanner_Logo_Azure_2024_320px.png` on light backgrounds; Dark Gray PNG as a single-color fallback
- **Favicon** → no file shipped — generate per the spec in Step 6 (white "S" on Azure circle)

### ⚠️ Legacy color caveat

The original Blue raster and vector files (`Spanner-Logo-Blue-Rev-01.png`,
`Spanner_Logo_Blue.svg`, `Spanner_Logo_Blue.eps`, and the Square/Rectangle Blue variants)
were produced in 2015 and use the **older "Spanner Blue" `#49B5CF`** — *not* the current
2024 Azure `#06A6ED`. They remain officially approved, but the `2024_Azure_Refresh/`
subfolder now carries SVG and PNG versions in current Azure. Default to the refresh
unless you specifically need a legacy match or an EPS for print.

The `Spanner-Color-Palette.png` file in the same folder is a **deprecated 2015 palette**
(includes yellow, red, purple) and must not be used as a brand reference. Always cite
`branding.md` for the authoritative palette.

### Inline SVG snippets

Both snippets are complete and self-contained — copy directly into HTML without reading
any external file. **The viewBox is `77.6 61.1 813.2 171` — cropped to the artwork.** The
2024 Azure export's own canvas (`0 0 965.951 275.986`) carries ~28% asymmetric padding;
never use it inline, or the wordmark renders ~38% smaller than its stated CSS height
(defect found and fixed 2026-06-09). With the cropped box, the stated px height IS the
rendered letter size: letter x-height = 0.74 × height, baseline = 0.26 × height above
the bottom edge. All 7 wordmark path shapes are identical; only the fill color differs.

**Azure logo — for light / white backgrounds:**

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="77.6 61.1 813.2 171"
     style="height:30px;width:auto;display:block;" aria-label="Spanner">
  <path fill="#06A6ED" d="M572.759,187.32h-21.136v-76.703c0-8.674-2.963-15.602-8.826-20.589c-5.364-4.575-13.002-7.195-20.941-7.195c-14.489,0-29.104,8.59-29.104,27.784v76.754h-21.132v-76.754c0-15.248,5.575-28.12,16.124-37.215c9.075-7.827,21.186-12.138,34.112-12.138c25.293,0,50.903,16.95,50.903,49.353V187.32z"/>
  <path fill="#06A6ED" d="M684.448,187.32h-21.136v-76.703c0-8.674-2.967-15.602-8.827-20.589c-5.364-4.575-13.002-7.195-20.942-7.195c-14.489,0-29.101,8.59-29.101,27.784v76.754h-21.134v-76.754c0-15.248,5.573-28.12,16.121-37.215c9.076-7.827,21.188-12.138,34.113-12.138c25.293,0,50.905,16.95,50.905,49.353V187.32z"/>
  <path fill="#06A6ED" d="M852.521,187.386h-21.26v-71.688c0-20.265,12.543-54.556,59.528-54.556v20.997c-37.691,0-38.269,27.88-38.269,33.559V187.386z"/>
  <path fill="#06A6ED" d="M258.583,61.111c-34.286,0-62.184,27.25-63.266,61.272h-0.051v109.674h21.216V176.61c0.003-1.514,1.554-3.118,3.755-2.055c10.649,7.623,24.687,13.181,38.346,13.181c34.966,0,63.313-28.341,63.313-63.31C321.897,89.456,293.55,61.111,258.583,61.111z M258.874,166.944c-23.202,0-42.012-18.806-42.012-42.01c0-23.201,18.811-42.01,42.012-42.01c23.204,0,42.014,18.809,42.014,42.01C300.888,148.138,282.078,166.944,258.874,166.944z"/>
  <path fill="#06A6ED" d="M460.001,122.383c-1.083-34.023-28.981-61.272-63.266-61.272c-34.967,0-63.314,28.345-63.314,63.315c0,34.969,28.347,63.31,63.314,63.31c13.643,0,27.661-5.542,38.306-13.152c2.1-1.07,3.606,0.298,3.796,1.735v11.014h21.216v-64.95H460.001z M396.443,166.944c-23.203,0-42.013-18.806-42.013-42.01c0-23.201,18.81-42.01,42.013-42.01c23.203,0,42.012,18.809,42.012,42.01C438.456,148.138,419.646,166.944,396.443,166.944z"/>
  <path fill="#06A6ED" d="M756.234,168.46c-20.442,0-34.448-10.403-39.725-28.432c-0.608-3.146,1.932-3.675,3.661-3.757h92.026v-0.036c7.008,0,8.572-0.729,8.485-8.01c0.019,0,0.032,0,0.049,0c-0.057-2.369-0.12-4.27-0.12-4.27c-0.146-34.795-27.731-62.119-62.473-62.119c-35.093,0-63.647,28.346-63.647,63.19c0,34.84,28.555,63.185,63.647,63.185c18.724,0,36.42-8.129,48.536-22.305l-15.729-13.388C782.279,162.65,769.631,168.46,756.234,168.46z M716.615,111.19c5.287-18.307,20.882-28.905,41.523-28.905c19.906,0,34.471,9.871,40.16,26.976h-0.002c0.034,0.107,0.075,0.216,0.107,0.325c0.37,1.19,1.242,4.792-1.666,5.26h-78.132C716.584,114.581,716.408,112.698,716.615,111.19z"/>
  <path fill="#06A6ED" d="M165.815,121.035c-9.249-4.466-18.616-5.222-27.675-5.954c-1.502-0.122-3.012-0.244-4.437-0.376l-1.661-0.167c-2.014-0.188-4.019-0.333-6.006-0.477c-7.147-0.513-13.32-0.958-18.42-3.421c-4.979-2.406-7.094-8.424-5.029-14.307c2.25-6.406,14.312-12.008,23.734-13.032c15.662-1.699,31.113,4.011,39.354,14.557l17.497-12.888c-13.02-16.662-35.743-25.424-59.292-22.859c-16.265,1.764-36.37,11.073-42.081,27.342c-5.656,16.113,1.084,33.051,16.032,40.279c8.963,4.327,17.92,4.971,26.583,5.596c1.829,0.131,3.672,0.263,5.438,0.428l1.663,0.167c1.607,0.15,3.21,0.28,4.804,0.409c7.637,0.617,14.232,1.148,19.71,3.794c4.978,2.405,7.091,8.421,5.027,14.305c-2.249,6.405-14.312,12.009-23.734,13.031c-14.759,1.604-33.386-3.481-41.938-18.411l-17.759,12.727c10.606,16.488,29.803,26.552,51.365,27.283c3.535,0.119,7.138-0.011,10.772-0.407c16.264-1.765,36.37-11.073,42.082-27.341C187.503,145.195,180.762,128.256,165.815,121.035z"/>
</svg>
```

**White logo — for dark / Navy backgrounds** (same paths, fill swapped to `#ffffff`):

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="77.6 61.1 813.2 171"
     style="height:30px;width:auto;display:block;" aria-label="Spanner">
  <path fill="#ffffff" d="M572.759,187.32h-21.136v-76.703c0-8.674-2.963-15.602-8.826-20.589c-5.364-4.575-13.002-7.195-20.941-7.195c-14.489,0-29.104,8.59-29.104,27.784v76.754h-21.132v-76.754c0-15.248,5.575-28.12,16.124-37.215c9.075-7.827,21.186-12.138,34.112-12.138c25.293,0,50.903,16.95,50.903,49.353V187.32z"/>
  <path fill="#ffffff" d="M684.448,187.32h-21.136v-76.703c0-8.674-2.967-15.602-8.827-20.589c-5.364-4.575-13.002-7.195-20.942-7.195c-14.489,0-29.101,8.59-29.101,27.784v76.754h-21.134v-76.754c0-15.248,5.573-28.12,16.121-37.215c9.076-7.827,21.188-12.138,34.113-12.138c25.293,0,50.905,16.95,50.905,49.353V187.32z"/>
  <path fill="#ffffff" d="M852.521,187.386h-21.26v-71.688c0-20.265,12.543-54.556,59.528-54.556v20.997c-37.691,0-38.269,27.88-38.269,33.559V187.386z"/>
  <path fill="#ffffff" d="M258.583,61.111c-34.286,0-62.184,27.25-63.266,61.272h-0.051v109.674h21.216V176.61c0.003-1.514,1.554-3.118,3.755-2.055c10.649,7.623,24.687,13.181,38.346,13.181c34.966,0,63.313-28.341,63.313-63.31C321.897,89.456,293.55,61.111,258.583,61.111z M258.874,166.944c-23.202,0-42.012-18.806-42.012-42.01c0-23.201,18.811-42.01,42.012-42.01c23.204,0,42.014,18.809,42.014,42.01C300.888,148.138,282.078,166.944,258.874,166.944z"/>
  <path fill="#ffffff" d="M460.001,122.383c-1.083-34.023-28.981-61.272-63.266-61.272c-34.967,0-63.314,28.345-63.314,63.315c0,34.969,28.347,63.31,63.314,63.31c13.643,0,27.661-5.542,38.306-13.152c2.1-1.07,3.606,0.298,3.796,1.735v11.014h21.216v-64.95H460.001z M396.443,166.944c-23.203,0-42.013-18.806-42.013-42.01c0-23.201,18.81-42.01,42.013-42.01c23.203,0,42.012,18.809,42.012,42.01C438.456,148.138,419.646,166.944,396.443,166.944z"/>
  <path fill="#ffffff" d="M756.234,168.46c-20.442,0-34.448-10.403-39.725-28.432c-0.608-3.146,1.932-3.675,3.661-3.757h92.026v-0.036c7.008,0,8.572-0.729,8.485-8.01c0.019,0,0.032,0,0.049,0c-0.057-2.369-0.12-4.27-0.12-4.27c-0.146-34.795-27.731-62.119-62.473-62.119c-35.093,0-63.647,28.346-63.647,63.19c0,34.84,28.555,63.185,63.647,63.185c18.724,0,36.42-8.129,48.536-22.305l-15.729-13.388C782.279,162.65,769.631,168.46,756.234,168.46z M716.615,111.19c5.287-18.307,20.882-28.905,41.523-28.905c19.906,0,34.471,9.871,40.16,26.976h-0.002c0.034,0.107,0.075,0.216,0.107,0.325c0.37,1.19,1.242,4.792-1.666,5.26h-78.132C716.584,114.581,716.408,112.698,716.615,111.19z"/>
  <path fill="#ffffff" d="M165.815,121.035c-9.249-4.466-18.616-5.222-27.675-5.954c-1.502-0.122-3.012-0.244-4.437-0.376l-1.661-0.167c-2.014-0.188-4.019-0.333-6.006-0.477c-7.147-0.513-13.32-0.958-18.42-3.421c-4.979-2.406-7.094-8.424-5.029-14.307c2.25-6.406,14.312-12.008,23.734-13.032c15.662-1.699,31.113,4.011,39.354,14.557l17.497-12.888c-13.02-16.662-35.743-25.424-59.292-22.859c-16.265,1.764-36.37,11.073-42.081,27.342c-5.656,16.113,1.084,33.051,16.032,40.279c8.963,4.327,17.92,4.971,26.583,5.596c1.829,0.131,3.672,0.263,5.438,0.428l1.663,0.167c1.607,0.15,3.21,0.28,4.804,0.409c7.637,0.617,14.232,1.148,19.71,3.794c4.978,2.405,7.091,8.421,5.027,14.305c-2.249,6.405-14.312,12.009-23.734,13.031c-14.759,1.604-33.386-3.481-41.938-18.411l-17.759,12.727c10.606,16.488,29.803,26.552,51.365,27.283c3.535,0.119,7.138-0.011,10.772-0.407c16.264-1.765,36.37-11.073,42.082-27.341C187.503,145.195,180.762,128.256,165.815,121.035z"/>
</svg>
```

To use `currentColor` (lets the CSS `color` property drive the fill — useful for
theme-adaptive contexts), replace every `fill="#06A6ED"` or `fill="#ffffff"` with
`fill="currentColor"` and set `color` on the SVG element or a parent.

## Step 8: Icons

Two styles — never mix within a single piece:
1. Simple Monoline — small spaces, topics/categories; white on dark backgrounds
2. Monoline + Azure Accent — scales well; Azure #06A6ED accent on monoline base

Building new icons: 100×100px grid, 4px stroke, 10% edge padding, 2px corner radius,
1px inner details, centered.

## Step 9: HTML Baseline

For all HTML artifacts, start with:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --navy:       #293A49;
    --white:      #FFFFFF;
    --azure:      #06A6ED;
    --orange:     #E2672A;
    --light-blue: #CAECF6;
    --light-gray: #D4D8DB;
  }
  body {
    font-family: 'Inter', 'Helvetica Neue', Helvetica, sans-serif;
    font-size: 17.33px;
    line-height: 25.33px;
    color: var(--navy);
    background: var(--white);
  }
</style>
```

Dark section: `background: var(--navy); color: var(--white);`

**Alternating section backgrounds:** use White `#FFFFFF` and Light Gray `var(--light-gray)` (#D4D8DB) only. Do not introduce custom off-palette grays like #F2F4F6, #F5F5F5, or #FAFAFA — these are off-brand.

Header/nav elements must always use `position: sticky; top: 0; z-index: 100;` unless the user explicitly requests a static header.

**Standard header lockup — "s07" (ratified from the header study, 2026-06-09).** Wordmark, pipe, and title in one `align-items: flex-end` row with the cropped-viewBox snippet:
- **Logo:** inline SVG at `height: 30px` (renders 22.2px letters), no margin.
- **Title:** `font-size: 22px; line-height: 22px; font-weight: 400;` color `rgba(255,255,255,0.88)` on navy (navy at 70% on light); `letter-spacing: 0.04em`; `margin-bottom: 5px` — this puts the type baseline on the wordmark baseline (formula: mb = 0.2614 × logoHeight − 0.1365 × fontSize).
- **Pipe:** Azure, `width: 1px; height: 28px; margin-bottom: 5px` — centered on the lowercase letter body (center C = 0.63 × logoHeight above the flex line; mb = C − height/2).
- **Gaps:** `gap: 24px` between logo, pipe, and title.
- **Bar:** `padding: 11px 0`, no fixed height (content-driven). **Title-only exception:** when the band holds only the lockup (a simple title, no nav links / search / actions), give it more presence with a taller bar — vertical padding ~15px → ~64px band (as on the EFM v2.0 page). Keep the lockup proportions; only the bar padding grows. Bands that also carry nav or actions keep the compact 11px bar.
To scale the whole lockup, multiply every value by one factor — proportions are the spec, pixels follow.

**Nav-links alignment in the same flex row:** Do NOT use `padding-bottom` on a scrollable nav-links container to create scroll clearance — with `flex-end` this pushes link text out of alignment with the logo and label. Do NOT put `margin-bottom` on the individual `<a>` elements inside the links container (this expands the container unpredictably). Instead, add `align-self: center` to the nav-links container itself. This overrides `flex-end` for that element only, centering the links vertically within the bar while the logo/pipe/label group remains baseline-aligned per spec.

```css
/* Correct pattern — s07 lockup */
.nav-inner  { display: flex; align-items: flex-end; padding: 11px 0; gap: 24px; }
.nav-logo   { flex-shrink: 0; }                                  /* svg height:30px, no margin */
.nav-pipe   { width: 1px; height: 28px; margin-bottom: 5px; background: var(--azure); }
.nav-label  { font-size: 22px; line-height: 22px; font-weight: 400; letter-spacing: 0.04em;
              margin-bottom: 5px; color: rgba(255,255,255,0.88); }
.nav-links  { flex: 1; align-self: center; }                     /* centers independently */
```
Sticky offsets on the page must match the resulting bar height (e.g. a toolbar's `top`).

## Step 9b: PPTX Slide Baseline (16:9 proposal decks)

Canvas and geometry (pptxgenjs):
- Layout: 13.3" × 7.5" (`defineLayout`), all coordinates in inches
- Slide margins: 0.55" left/right; body text may run full width (12.2")
- Footer: 9pt Light Gray #D4D8DB at y 7.06" — "Confidential | Spanner, Inc."
  left, page number right; pipes Azure #06A6ED
- Type: slide titles 20pt lowercase Regular; body 13pt with `lineSpacing: 19`;
  lead-in emphasis 14pt with `lineSpacing: 22`; overlines 11pt Bold lowercase

**Critical — zero the text insets.** PowerPoint default text-box insets
(~0.1" left, ~0.05" top/bottom) silently break edge and baseline alignment,
and preview renderers (LibreOffice) under-report them. Set `margin: 0` on
every `addText` call so geometry is deterministic across PowerPoint,
LibreOffice, and HTML mirrors.

**PPTX header lockup (equivalent of the Step 9 s07 pattern).** Updated 2026-09-11 for the
`2026_Spanner_Logo_Files/` PNGs, which are ink-tight: letterforms span **0%–74%** of image
height (74% is the baseline, the rest is the p descender) and the x-band optical center is at
**37%**. The placed image is therefore *smaller* than before for the same rendered wordmark —
0.279" replaces 0.45", and the visible width is unchanged at 1.326".

```js
// 2026 files — aspect 813.16 / 170.95 = 4.757, letters 0%–74% of height
const lgH = 0.279, lgW = lgH * (813.16 / 170.95), lgX = 0.55;
const lgY = 0.475 - 0.37 * lgH;            // optical center on band center
const optC = lgY + 0.37 * lgH;             // letterform optical center
// pipe: Azure, 0.016" × 0.22", centered on optC
{ x: lgX + lgW + 0.18, y: optC - 0.11, w: 0.016, h: 0.22 }
// title: 20pt lowercase, valign middle, margin 0, centered on optC
{ x: lgX + lgW + 0.36, y: optC - 0.275, h: 0.55, valign: "middle", margin: 0 }
```
**If a deck still places a padded 2024 PNG**, its numbers are `lgH = 0.45`,
`lgW = lgH * (965.951 / 275.986)` and optical center `0.45` — do not mix the two sets, and
do not swap the image file without also swapping the maths, or the wordmark changes size.

**Bullets on slides.** Azure dot markers as 0.07" ellipse shapes; dot center
on the first text line center (y + 0.097" at 19pt line spacing with zero
insets); text box starts 0.18" after the dot's left edge (tight gap ≈ 0.11");
bold lead + " — " + regular description.

**Approved deck background variants.** Two sanctioned slide systems:
1. *Light content* — Navy header band + white wordmark; white body, navy text;
   light-blue cards with azure left rules for scannable lists.
2. *Full navy* — entire slide Navy, white text, single-column, no card boxes;
   azure dot bullets; light-gray footers. Preferred for proposal decks
   (established Testco 2026-06). Do not "correct" a full-navy deck to white.

**QA rule.** Always verify final geometry in PowerPoint (or zero all insets) —
LibreOffice-rendered previews differ on insets and substitute fonts when Inter
is not installed.

## Step 10: Compliance Checklist

Before delivering any visual output, verify:

- [ ] Font is Inter — not system-default serif, Arial, or other sans-serif
- [ ] Type sizes match the standard scale — headline ~66.67px, body ~17.33px; nothing smaller than the 12px micro tier (no off-scale sizes like 13px)
- [ ] Line-height is an absolute value (25.33px for body), not a unitless multiplier like 1.65
- [ ] Micro / fine-print text (12px) clears AA — Navy #293A49 or no lighter than #65717C on white; never opacity-dimmed Navy or any tint below #65717C
- [ ] Pipe delimiters have 3 spaces each side, equal to the eye — measured glyph-to-glyph, not box-to-box
- [ ] Text color is Navy #293A49, not black #000000 or charcoal
- [ ] Background is White or Navy (or Light Gray #D4D8DB as neutral — no custom grays)
- [ ] Navy backgrounds paired only with White text
- [ ] Azure #06A6ED is the only blue — no other blue values anywhere
- [ ] No failing color pairings
- [ ] At most one accent method per surface
- [ ] No ALL CAPS except abbreviations — and no `text-transform: uppercase` anywhere in CSS
- [ ] Deck/report headers in lowercase
- [ ] No green of any shade (check badges, availability states, price savings, status indicators)
- [ ] No teal
- [ ] Pipe delimiters are Azure #06A6ED even on dark/Navy backgrounds
- [ ] Header/nav is sticky (`position: sticky; top: 0`) unless explicitly told otherwise
- [ ] Header lockup is s07: inline SVG with cropped viewBox `77.6 61.1 813.2 171` at `height:30px`, title 22px/w400/88%-white baseline-aligned (mb 5), pipe 28px/mb 5, gaps 24px, bar `padding: 11px 0` (title-only bands: taller, ~15px → ~64px)
- [ ] No padded viewBox (`0 0 965.951 275.986`) anywhere inline
- [ ] PPTX: `margin: 0` on every addText; header lockup via the 2026 files — `lgH = 0.279`, aspect 4.757, optical center 37% (padded 2024 files only for pre-existing decks); final check rendered in PowerPoint
- [ ] Nav-links container uses `align-self: center`, not `padding-bottom`, for vertical placement
- [ ] If a logo file was used: pulled from `Logo/2026_Spanner_Logo_Files/` and matched to background (Azure or Navy on light, White on dark). The older package is archival — the legacy-blue caveat applies if anything from it was used

## Tagline

"what's next." — always Azure #06A6ED, lowercase, never in quotes.
Include trailing period when standalone; omit mid-sentence unless at sentence end.
