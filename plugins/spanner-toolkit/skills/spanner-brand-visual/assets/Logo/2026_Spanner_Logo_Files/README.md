# Spanner Logo Files — 2026 set

**Use these.** One flat folder, no subfolders, correct geometry in every file.

Everything here is the same artwork that has been the Spanner wordmark since 2015 — the
identical seven curves, unmodified. What changed is the box around them and how colour is
applied. Nothing was redrawn and no colour was re-sampled.

## Files

| File | Use for |
|---|---|
| `Spanner-Wordmark-Azure.svg` | **Inline HTML, web, anything CSS-sized.** Default Azure `#06A6ED` |
| `Spanner-Wordmark-White.svg` | Same, defaulting to white — for `<img>` on dark, or where inheritance is inconvenient |
| `Spanner-Wordmark-Navy.svg` | Same, defaulting to Navy `#293A49` — formal documents, single-colour work |
| `Spanner-Wordmark-{Azure,White,Navy}-320.png` | Email signatures, small web placements |
| `Spanner-Wordmark-{Azure,White,Navy}-640.png` | Standard web and slide placements |
| `Spanner-Wordmark-{Azure,White,Navy}-1280.png` | Hero placements, large slides, 2× retina |
| `Spanner-Wordmark-White.eps` | Print on Navy or dark photographic backgrounds |
| `Spanner-Wordmark-DarkGray.eps` | Print, single-colour reproduction |
| `Spanner-Wordmark-Blue-Legacy2015.eps` | **Legacy `#49B5CF` only.** The sole EPS in a brand colour until a designer re-exports an Azure one. Do not use for new work |

All three SVGs are byte-identical apart from one hex value in `svg:root`.

## What was wrong with the files this set replaces

The 2024 Azure SVG was produced by recolouring the 2015 Blue export, and inherited that
file's **padded artboard**: `viewBox="0 0 965.951 275.986"` around artwork that occupies only
`813.16 × 170.95`, offset 77.62 from the left and 61.11 from the top. Ink filled **61.9%** of
the declared height, and the padding was asymmetric — 61.11 above the letters, 43.93 below.

Measured consequences:

- `height:45px` rendered a **27.9px** wordmark. The same CSS on the 2015 white-only SVG
  rendered a true 45px, which is why identical header markup produced visibly different
  logos depending on which file it used.
- The 2024 PNG renders were generated from that padded SVG, so they baked the dead space
  into raster. The old 640px file measured **540 × 114 of ink in a 640 × 183 canvas**. A
  320px placement yielded a ~270px wordmark sitting high in its box.
- The asymmetry also shifted the baseline, so alignment offsets tuned against the padded
  file stopped working the moment it was cropped.

**The 2015 EPS and PNG files never had this problem** (`%%HiResBoundingBox: 0 0 813.1626
170.9463`, ink filling 100%). It was introduced by the 2024 SVG re-export and inherited by
everything rendered from it.

## What this set does differently

1. **`viewBox="0 0 813.16 170.95"` — the artwork exactly.** Paths translated by
   `(-77.63, -61.11)`. Ink fills 100% of both axes in every file here, verified.
2. **No `width`/`height` attributes on the SVGs.** The 2024 file declared
   `width="965.951px" height="275.986px"`, an intrinsic size that wins wherever CSS is not
   driving — `<img>`, Slides and PowerPoint import, paste into Office.
3. **Colour through `fill="currentColor"`**, defaulted by `svg:root{color:…}`. `:root`
   matches the `<svg>` only when the file *is* the document, so each renders its own colour
   standalone or via `<img>`, but inherits `color` when inlined into HTML. Inlined on a page
   that sets no colour at all it renders black — set `color` wherever you place it.
4. **PNGs re-rendered from the corrected SVGs**, so 320 px of image is 320 px of wordmark.

## The one constant worth knowing

`height` is the **full ink**, which includes the descender of the **p**.

- letter body (what reads as the size of the logo) = **0.740 × height**
- baseline sits **0.260 × height** above the bottom edge

The s07 header lockup's 30px box therefore gives 22.2px letters. For placing the **PNGs**,
letterforms now span the full image height and the optical centre is at **37%** of image
height — the old "22%–68%, optical centre 45%" figures describe the padded 2024 renders and
do not apply to anything in this folder.

## Aspect ratio

`813.16 / 170.95 = 4.757`. Any placement maths should use that, not the padded 3.500.

---

_Created 2026-09-11. Source geometry: `0_Spanner Logo Package (External Sharing OK)/2024_Azure_Refresh/Spanner_Logo_Azure_2024.svg`, curve data verified byte-identical. The older package is left in place untouched for archival and for matching pre-2026 collateral._
