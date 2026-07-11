---
name: torque-design-language
description: Applies Torque — SpannerOS's product-interface design language (glass panels over Spanner navy/paper, var-driven theming, data-dense glass UI) — to any SpannerOS screen, internal tool, dashboard, or interactive mockup. Use whenever building or styling SpannerOS app surfaces, portal tools, or HTML mockups in the Torque style: "build this in Torque", "use the unbound style", "SpannerOS skin", "make the dark/light app version", "glass style", or any interface-*-unbound mockup work. NOT for client-facing brand collateral, documents, decks, or marketing pages — those follow spanner-brand-visual. When in doubt between the two: product UI = Torque, everything else = brand.
---

# Torque — the SpannerOS interface design language

**Torque** is the design language for SpannerOS product surfaces — the working end of the spanner. It was developed June 2026 as the "unbound" exploration family (`SpannerOS/mockups/interface-*-unbound*.html`, 14 reference pages) and is now codified here. Torque uses **Spanner colors only** but deliberately does not follow the document/marketing brand guidelines (no s07 logo lockup, no 120% type scale) — it is a parallel system for interactive product UI. `spanner-brand-visual` still governs documents, decks, reports, and portal/marketing pages.

**Reference implementations (canonical):** any `interface-*-unbound*.html` in `SpannerOS/mockups/`. Richest examples: `interface-11-guided-unbound.html` (stepper, charts, choreography), `interface-9d-unbound.html` (dense grid + charts), `interface-1-unbound.html` (dashboard cards).

---

## 1 · Principles

1. **Calm glass over navy or paper.** One quiet page surface (Spanner navy in dark, warm paper-gray in light) with translucent glass panels floating on it. Two radial glows give the page depth; nothing else decorates.
2. **Color is information, never decoration.** Azure means interactive/actual. Orange means warning/over. Amber means estimate. Green means confirmed/on-target. Gray family means time-away/NB/internal. If a color doesn't carry one of those meanings, it doesn't appear.
3. **Density with air.** Torque pages are operator tools — they show a lot. Density comes from small, precise type and hairlines; breathing room comes from panel gaps and generous page margins, never from hiding data.
4. **The chrome teaches.** Labels explain themselves ("↔ = on target (within ±4h or ±$1k)"), footers cite the functional reference, flags say why they matter. A new TPL should be able to read any screen cold.
5. **Motion is state change.** Things animate only when state changes — a verification line appearing, a panel collapsing, a ring filling. Nothing moves at rest. 0.15–0.3s ease; choreographed sequences stagger ~250–330ms per item.

---

## 2 · Canonical tokens

Copy this block verbatim into every Torque page. **Light is the default** (`<html data-theme="light">`). Dark uses **Spanner navy `#293A49`** as the page surface.

```css
html[data-theme="dark"] {
  --bg:#293A49;                       /* Spanner navy — the dark page surface */
  --bgglow1:rgba(6,166,237,0.10);     /* azure radial glow, top-right */
  --bgglow2:rgba(226,103,42,0.05);    /* orange radial glow, top-left */
  --panel:rgba(255,255,255,0.045);    /* glass panel */
  --panel2:rgba(255,255,255,0.075);   /* raised glass (chips, day cells) */
  --line:rgba(255,255,255,0.10);      /* hairlines + borders */
  --tx:#E8EEF4;                       /* primary text */
  --mut:#93A3B2;                      /* secondary text */
  --dim:#5E6E7D;                      /* tertiary text, axis labels */
  --azure:#1FB2F5;                    /* brand azure, lifted for dark contrast */
  --orange:#ED7A40;                   /* brand orange, lifted */
  --amber:#D9A514;                    /* data-palette amber (estimate series) */
  --green:#2EC592;                    /* brand green, lifted */
  --lblue:#CAECF6;                    /* light blue accents */
  --shadow:none;                      /* dark theme uses glows, not shadows */
  --glow:0 0 36px rgba(6,166,237,0.07);
  --inbg:rgba(0,0,0,0.25);            /* input / inset background */
  --stick:#314254;                    /* opaque bg for sticky table columns */
}
html[data-theme="light"] {
  --bg:#F4F7F9;
  --bgglow1:rgba(6,166,237,0.06);
  --bgglow2:rgba(226,103,42,0.03);
  --panel:#FFFFFF;
  --panel2:#FFFFFF;
  --line:#DCE3E8;
  --tx:#293A49;                       /* navy is the text color on light */
  --mut:#6B7A8A;
  --dim:#97A2AC;
  --azure:#06A6ED;                    /* true brand azure */
  --orange:#E2672A;                   /* true brand orange */
  --amber:#B58A10;                    /* amber darkened for light-bg contrast */
  --green:#0B7C58;                    /* true brand green */
  --lblue:#CAECF6;
  --shadow:0 1px 3px rgba(41,58,73,0.08), 0 8px 28px rgba(41,58,73,0.05);
  --glow:var(--shadow);
  --inbg:#F4F7F9;
  --stick:#FFFFFF;
}
```

Page background recipe (always):

```css
body {
  background:
    radial-gradient(1100px 500px at 75% -10%, var(--bgglow1), transparent 60%),
    radial-gradient(800px 420px at 8% 8%, var(--bgglow2), transparent 55%),
    var(--bg);
  transition: background 0.3s, color 0.3s;
}
```

**Brand-color discipline:** only Spanner colors appear — navy, azure, orange, green, light-blue, white/grays — plus the **ratified extended data palette** for project identity and chart series (amber #D9A514, violet #6A5FA8, berry #B23A6F, the Tin blue ramp, green #1E7D4F, slate, etc. — see `spanner-data-palette.html`). The reserved **gray semantic family** (silver #B9C1C8 DTO/holiday · gray #97A2AC NB · steel #76828D OOO · charcoal #55606B leave/furlough) keeps its meanings in both themes. **Red stays reserved for alerts** and is almost never on a Torque page.

---

## 3 · Theming rules

- `<html data-theme="light">` is the default. The toggle lives at the far right of the top bar (`☾ dark` / `☀ light`).
- Preference persists in `localStorage` under the shared key **`sos-torque-theme`** — one choice follows the user across every Torque page.
- **All SVG/chart colors must reference tokens** via `style="fill: var(--azure)"` / `style="stroke: var(--line)"` (never `fill="#..."` attributes). This is what makes the theme toggle restyle every chart instantly with no re-render. Fixed identity colors (project palette hexes, the gray family) are the only allowed literals.
- Terminal/trace surfaces (verification logs) stay dark in **both** themes — terminals are dark.

Toggle boilerplate:

```js
var root = document.documentElement;
try { root.dataset.theme = localStorage.getItem('sos-torque-theme') || 'light'; } catch(e){}
window.toggleTheme = function(){
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('sos-torque-theme', root.dataset.theme); } catch(e){}
  syncBtn();
};
```

---

## 4 · Typography

- **Inter** for everything; **JetBrains Mono** for IDs (`NEU-001`), Harvest entry numbers, client codes, terminal traces, and rank numbers.
- Scale (px): page title **24–27/800**, panel heading **17–21/800**, big stat **19–30/800**, body/data **13–14.5/400–600**, secondary **11.5–12.5**, section/axis labels **10–11/700–800 with 0.07–0.09em letter-spacing** (these small caps-feel labels are written in CAPS — the one place caps are used), chart labels **8.5–9.5**.
- `font-variant-numeric: tabular-nums` on **every** numeric surface (tables, stats, day cells).
- `-webkit-font-smoothing: antialiased` on body. Negative letter-spacing (−0.01 to −0.02em) only on titles ≥21px.

---

## 5 · Surfaces & layout

- **Top bar:** sticky, blurred (`backdrop-filter: blur(18px)`, bg = `color-mix(in srgb, var(--bg) 78%, transparent)`), 1px bottom hairline. Contains: brand wordmark `SPANNER<i>OS</i>` (14px/800, 0.14em tracking, the `OS` in azure — **no logo SVG on Torque pages**), breadcrumb, page controls, theme toggle.
- **Sticky sub-strips** (stat constellations) blur the same way. **Never hardcode sticky offsets — measure the bar's `offsetHeight` at runtime** (and re-measure on resize / use ResizeObserver). Same rule for chart geometry: measure rendered columns, never assume widths.
- **Panels:** 16px radius, 1px `var(--line)` border, `var(--panel)` fill, `var(--shadow)` (light) / nothing-or-glow (dark). Padding 13–17px. Panel title = the small caps label, with inline explanatory text in `var(--mut)` after it.
- **Page width:** max 1140–1280px, 26px side padding. Grids: CSS grid with 14px gaps; 12-col spans for dashboards.
- **Inputs:** `var(--inbg)` fill, 9–10px radius, 1px line border; focus = azure border, no outline ring. Inline hints use a 2.5px azure left border on an `--inbg` strip.
- Azure focus/selection glow: `box-shadow: 0 0 16–24px rgba(6,166,237,0.12–0.18)` plus azure border.

---

## 6 · Components

- **Buttons.** Primary: azure fill, white 800 text, 11px radius, `box-shadow: 0 4px 22px rgba(6,166,237,0.3)`; hover = `filter: brightness(1.07)`. Ghost: 1px line border, muted text. Acknowledge/warning action: orange fill. Pill actions (nudges): 999px radius, azure-tinted fill + border.
- **Chips & pills:** 999px radius; status colors as 12% tint background + 35% tint border + colored text (`color-mix` does the tints). States: pending=orange, approved/ok=green tint, drifted=solid orange + white text.
- **Segmented controls:** pill group on `--inbg`/panel, 2px padding, active segment = azure fill white text.
- **Tables:** hairline rows only (`--line`), 10px caps headers in `--dim`, right-aligned numerics, hover row = 5% azure tint. Sticky first column uses opaque `var(--stick)`.
- **Avatars:** rounded-square (9–12px radius), azure 14% tint fill + 30% tint border, azure initials. Variants: amber tint = expense rows, orange tint = pending/placeholder.
- **Steppers & rails** (guided flows): numbered circles — done = azure fill + white check, current = azure border + glow, todo = line border; clickable; pair with a progress ring (`stroke-dasharray` arc) in the bar.
- **Flags:** glass card, orange border (info variant: line border + azure icon), round icon chip, body in `--mut` with `--tx` bolds.
- **Day/grid cells:** rounded 7–10px tinted cells — azure 16% = at-target, orange 18% = surge band, solid orange = over; em-dash in faded `--dim` for empty (never 0).
- **Terminal trace:** JetBrains Mono 11px on near-black glass with azure border tint; lines fade-translate in, staggered ~260–280ms; ✓ green, ⚠ orange, ▸ headers azure.
- **Persistent comment bar / command bar:** fixed bottom, blurred like the top bar; body gets matching `padding-bottom`.

---

## 7 · Charts

- **Hand-rolled inline SVG only** — no chart libraries (alignment + theming control; same rationale as the planner grid decision).
- **Series semantics (fixed):** actual = `var(--azure)` (solid, heaviest 2.4–2.6 stroke, area fill at 13–16% tint); estimate/forecast = `var(--amber)`; estimate-from-now = `var(--mut)`; baseline = `var(--tx)` dashed at 0.5 opacity; budget/zero reference = `var(--orange)` dashed; gray stepped area = estimate envelope on bar charts.
- Gridlines = `var(--line)` 1px; axis labels = `var(--dim)` 8.5px; key values annotated directly on the chart in series color, 700 weight.
- Highlight band for "this/reviewed week" = azure 8% tint rect behind the plot.
- Approved-actuals rule carries everywhere: the actual series stops at the last approved week with a dot.
- In-progress bars: azure at 28–38% opacity with 1px azure stroke.
- Tooltips/crosshairs sync across all chart panels on a page (shared hover registry pattern — see interface-9d).

---

## 8 · Data-visibility rules (carry over from SpannerOS)

- **Money is role-gated**: member/contractor surfaces show hours only — no rates, $, budgets, or EAC anywhere (7U and 8U are the reference money-free pages). Gate server-side in the real app; in mockups, state it in the footer.
- The gray family is never assigned to a client; Tin owns the blues; >14 series aggregate to "other" (data-palette rules apply unchanged).
- Status language: green **on track** · amber **watch** · orange **at risk** — red is not a status.

---

## 9 · Voice on Torque pages

Lowercase labels and headings except the small-caps label rows; sentence-case explanatory text in `--mut`; every page footer states what the page is, its theme behavior, and its **functional reference** (the mockup or build target that owns the interaction contract). Explain rules inline where the user meets them ("↔ = on target (within ±4h or ±$1k)").

---

## 10 · Build checklist

Before presenting any Torque page:

- [ ] Token block copied verbatim; `data-theme="light"` default; toggle present and persisting to `sos-torque-theme`
- [ ] Dark page surface is Spanner navy `#293A49`; both themes checked
- [ ] All SVG colors via `style="...var(--x)"` (toggle restyles charts with no re-render)
- [ ] Sticky offsets measured, not hardcoded
- [ ] Numbers in tabular-nums; em-dash (not 0) for empty cells
- [ ] Color = meaning audit: nothing azure that isn't interactive/actual, nothing orange that isn't a warning/over
- [ ] Money gated on member-visible surfaces
- [ ] Footer: design-exploration note + functional reference
- [ ] JS syntax-checked; every `getElementById` target exists

---

## 11 · Relationship to other Spanner standards

| Surface | Standard |
|---|---|
| SpannerOS app screens, internal tools, interactive mockups | **Torque** (this skill) |
| Documents, decks, PDFs, reports, one-pagers | `spanner-brand-visual` (s07 lockup, 120% type scale) |
| Plan/notes infographic pages, portal article pages | `spanner-brand-visual` |
| Data series & project identity colors (everywhere) | `spanner-data-palette.html` (shared by both) |

History: Torque began as the "unbound" exploration (June 11, 2026, weekly-review variants). The 14 reference pages keep their `-unbound` filenames; the language itself is named Torque.
