# Spanner Logo — 2024 Azure Refresh

These files are color-corrected versions of the wordmark using the **current 2024 Azure `#06A6ED`**.

## Why this folder exists

The original `Spanner-Logo-Blue-Rev-01.png`, `Spanner_Logo_Blue.svg`, and `Spanner_Logo_Blue.eps` files in the parent folder were produced in 2015 and use a legacy "Spanner Blue" of `#49B5CF` — a slightly more cyan/teal blue that doesn't match the current 2024 brand palette.

Both blues are recognizably "Spanner blue" at a glance, but they're visibly different when placed side by side or next to current-Azure accents (pipes, headers, highlights). This folder gives you a current-Azure version for any deliverable where the rest of the surface uses 2024 brand color.

## Files

| File | Format | Notes |
|---|---|---|
| `Spanner_Logo_Azure_2024.svg` | SVG, vector | Authoritative source geometry. **Padded artboard — see below.** For placement use `../../2026_Spanner_Logo_Files/` |
| `Spanner_Logo_Azure_2024_320px.png` | PNG, transparent | Email signatures, small web placements |
| `Spanner_Logo_Azure_2024_640px.png` | PNG, transparent | Standard web/slide placements |
| `Spanner_Logo_Azure_2024_1280px.png` | PNG, transparent | Hero placements, large slides, 2x retina |

## When to use these vs. the originals

- **Use these (2024 Azure)** when the deliverable also uses current Azure as an accent color — decks, web pages, emails, dashboards, anything styled per `branding.md`
- **Use the originals (legacy `#49B5CF`)** when matching pre-2024 collateral that still circulates externally, or when a designer requests the historical files for archival reasons

## Still missing

- **EPS in current Azure** — would need to be re-exported by a designer from the .ai source in `1_Native Logo Files/`. Until that's done, use the SVG for vector workflows
- **Refreshed Square / Rectangle / White-on-Blue panel composites** — these legacy framed variants haven't been regenerated yet
- **Updated `1_Native Logo Files/` .ai sources** — designer task

## Padded artboard — read this before placing these files

`Spanner_Logo_Azure_2024.svg` was recoloured from `2_Export Logo Files/Spanner_Logo_Blue.svg`,
and inherited that file's **padded artboard**: the viewBox is `0 0 965.951 275.986` but the
artwork occupies only `813.16 x 170.95` of it, offset 77.62 from the left and 61.11 from the
top. The ink therefore fills just **61.9% of the declared height**, and the padding is
asymmetric — 61.11 above the letters, 43.93 below.

Two consequences, both measured:

1. **`height:45px` renders a 27.9px wordmark.** The already-cropped
   `150810_Spanner_Logo_White-only.svg` renders a true 45px from identical CSS, which is why
   the same header markup produced visibly different logos depending on which file it used.
2. **The asymmetry shifts the baseline**, so any pipe/label offsets tuned against the padded
   file stop working the moment it is cropped. That is why the s07 header lockup re-derives
   them from geometry rather than adjusting the old 21/14/11 values.

**This is fixed in `Logo/2026_Spanner_Logo_Files/`, which is now the current set** — the same
seven curves translated by `(-77.63, -61.11)` into `viewBox="0 0 813.16 170.95"`, `width`/`height`
attributes removed so CSS always wins, `fill="currentColor"` so one file covers azure, navy and
white surfaces, and the PNGs re-rendered so 320px of image is 320px of wordmark. Go there for
anything new; this folder is retained for archival and for matching pre-2026 collateral.

**Sizing constant:** `height` is the full ink, which includes the descender of the **p**. The
letter body — what reads as the size of the logo — is **0.740 x height**. The s07 lockup's
30px box therefore gives 22.2px letters.

`Spanner_Logo_Blue.svg` has the same padded artboard. It is legacy `#49B5CF` and is not being
corrected; use the 2024 files.

## Generation notes

The SVG was produced by replacing every `#49B5CF` fill in `2_Export Logo Files/Spanner_Logo_Blue.svg` with `#06A6ED`. Path geometry is identical to the original — no shapes were modified, only color. PNG renders were generated from the new SVG via cairosvg at the widths above with transparent background.

The 2026 set was derived from `Spanner_Logo_Azure_2024.svg` on 2026-09-11 by translating the
seven paths into a cropped viewBox. Geometry is byte-for-byte the same curve data — no shapes were
modified, no colour was re-sampled. Verified in-browser: ink fills 100% of the viewBox in both axes
with no clipping, each file renders its own colour standalone, and inherits `color` when inlined.
