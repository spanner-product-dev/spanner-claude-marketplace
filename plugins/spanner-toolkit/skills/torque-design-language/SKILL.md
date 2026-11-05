---
name: torque-design-language
description: Applies Torque — SpannerOS's product-interface design language (glass panels over Spanner navy/paper, var-driven theming, data-dense glass UI) — to any SpannerOS screen, internal tool, dashboard, or interactive mockup. Use whenever building or styling SpannerOS app surfaces, portal tools, or HTML mockups in the Torque style: "build this in Torque", "use the unbound style", "SpannerOS skin", "make the dark/light app version", "glass style", or any interface-*-unbound mockup work. NOT for client-facing brand collateral, documents, decks, or marketing pages — those follow spanner-brand-visual. When in doubt between the two: product UI = Torque, everything else = brand.
---

# Torque — the SpannerOS interface design language

_Skill copy of `Mason-Claude/Projects/SpannerOS/specs/torque-design-language.md` as of 2026-11-04 (through R-128). That file is the source of truth; if you can reach it, read it and prefer it over this copy._

**Torque** is the design language for SpannerOS product surfaces — the working end of the spanner. It was developed June 2026 as the "unbound" exploration family (`mockups/interface-*-unbound*.html`, 14 reference pages) and is now codified here. Torque uses **Spanner colors only** but deliberately does not follow the document/marketing brand guidelines (no s07 logo lockup, no 120% type scale) — it is a parallel system for interactive product UI. `spanner-brand-visual` still governs documents, decks, reports, and portal/marketing pages.

**Reference implementations (canonical):** any `interface-*-unbound*.html` in `mockups/`. Richest examples: `interface-11-guided-unbound.html` (stepper, charts, choreography), `interface-9d-unbound.html` (dense grid + charts), `interface-1-unbound.html` (dashboard cards).

---

## 1 · Principles

1. **Calm glass over navy or paper.** One quiet page surface (Spanner navy in dark, warm paper-gray in light) with translucent glass panels floating on it. Two radial glows give the page depth; nothing else decorates.
2. **Color is information, never decoration.** Azure means interactive/actual. Orange means warning. Amber means watch. Gray means estimate and forecast, drawn so it cannot be mistaken for the reserved gray family of time-away/NB/internal. Green means confirmed/on-target. If a color doesn't carry one of those meanings, it doesn't appear, and every color, tint or legend entry is explained on the screen.
3. **Density with air.** Torque pages are operator tools — they show a lot. Density comes from small, precise type and hairlines; breathing room comes from panel gaps and generous page margins, never from hiding data.
4. **The chrome teaches.** Labels explain themselves ("↔ = on target (within ±4h or ±$1k)"), footers cite the functional reference, flags say why they matter. A new TPL should be able to read any screen cold.
5. **Motion is state change.** Things animate only when state changes — a verification line appearing, a panel collapsing, a ring filling. Nothing moves at rest. 0.15–0.3s ease; choreographed sequences stagger ~250–330ms per item.

---

## 2 · Canonical tokens

Copy this block verbatim into every Torque page. **Both themes ship and the default follows the system setting** (`data-theme` is set before first paint from the person's choice or the system; Mason, 2026-10-22 — see §3). Dark uses **Spanner navy `#293A49`** as the page surface. The app's copy is `app/(os)/torque.css` in `spanner-planner`, ported verbatim; change the two together.

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
  --amber:#D9A514;                    /* data-palette amber (watch status; no longer the estimate) */
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
  --amber:#B58A10;                    /* amber darkened for light-bg contrast (amber text still fails 4.5:1 in light: pending) */
  --green:#0B7C58;                    /* true brand green */
  --lblue:#CAECF6;
  --shadow:0 1px 3px rgba(41,58,73,0.08), 0 8px 28px rgba(41,58,73,0.05);
  --glow:var(--shadow);
  --inbg:#F4F7F9;
  --stick:#FFFFFF;
}
```

**Estimate token.** The estimate and forecast series use one gray token, `--est`, defined globally for both themes (today it exists only under `.pch-g` and `.w4ch`, and a `var(--est, var(--amber))` fallback paints some screens amber: that fallback goes). Its exact value and the treatment that separates it from the reserved gray family are pending.

**System and header tokens** (added by the design-system pass 2026-09-30 and the navy header 2026-10-05; both themes unless noted):

```css
:root {
  --r-panel:16px; --r-in:10px; --r-btn:11px; --r-chip:999px; --r-cell:8px;   /* radii */
  --sp1:4px; --sp2:8px; --sp3:12px; --sp4:16px; --sp5:20px; --sp6:24px; --sp8:32px; --sp10:40px;
  --navw:232px; --navw-c:64px; --railw:320px;   /* --railw is the default; the rail is draggable (§12) */
  --s:1;                                   /* type factor: edit = 1, present = 1.125 */
  --fs-title:calc(26px*var(--s)); --fs-h2:calc(20px*var(--s)); --fs-body:calc(16px*var(--s));
  --fs-data:calc(15.5px*var(--s)); --fs-small:calc(15px*var(--s)); --fs-cap:calc(12.5px*var(--s));
  --fs-chart:calc(11px*var(--s)); --fs-big:calc(40px*var(--s));
  --gray-dto:#B9C1C8; --gray-nb:#97A2AC; --gray-ooo:#76828D; --gray-leave:#55606B;
  --red-alert:#D94040;
  --e1:var(--shadow); --e2:0 2px 6px rgba(41,58,73,.10),0 16px 40px rgba(41,58,73,.10);
  /* the header bar: navy in every skin and both themes (§5) */
  --hdr-bg:#293A49; --hdr-tx:#FFFFFF; --hdr-soft:rgba(255,255,255,.85); --hdr-mut:rgba(255,255,255,.74);
  --hdr-ctl:rgba(255,255,255,.06); --hdr-line:rgba(255,255,255,.45); --hdr-off:rgba(255,255,255,.4);
  --hdr-accent:#06A6ED; --hdr-link:#8FD6F7; --hdr-focus:#8FD6F7;
  --hdr-on-bg:#8FD6F7; --hdr-on-tx:#1D2B37;   /* selected segment: white-on-azure fails 4.5:1 */
}
html[data-theme="dark"] {
  --hdr-bg:#1D2B37;                        /* darker than the #293A49 page so the bar still reads as a bar */
  --e2:0 0 0 1px rgba(255,255,255,.08),0 18px 48px rgba(0,0,0,.35);
}
html[data-mode="present"] { --s:1.125; }
```

The brand skin overrides these same names under `html[data-skin="brand"]` (design-system spec §8); it is not a second token set.

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

- **The default theme follows the system setting everywhere** — the shell, sign-in, /planning and time entry (Mason, 2026-10-22; R-67, replacing the dark default of 2026-10-07). With nothing stored, `data-theme` resolves from `prefers-color-scheme`, set before first paint so a light-theme person never sees a dark first frame. No screen forces dark or light.
- The choice is a **three-way select, not a toggle**: dark ☾ · light ☀ · system ◐ ("system" tracks `prefers-color-scheme` live). It lives in the account menu in the bottom-left dock (R-05).
- One choice follows the person across every screen: `localStorage` key **`sos-os-theme`** (values `dark` / `light` / `system`). The old key `sos-torque-theme` is still read as a fallback when nothing newer is stored, and is folded into the new key the next time anyone picks. App code: `lib/theme-pref.ts`.
- A **pre-paint boot script** sets `data-theme` before the first frame, so nobody sees a flash of the wrong theme. It must repeat the same read-and-resolve logic as `lib/theme-pref.ts`; keep the two in step.
- Every surface is checked in both themes, and light is a release gate. Form fields use theme colors and native controls get a matching `color-scheme` for the resolved theme (R-68).
- **All SVG/chart colors must reference tokens** via `style="fill: var(--azure)"` / `style="stroke: var(--line)"` (never `fill="#..."` attributes). This is what makes the theme toggle restyle every chart instantly with no re-render. Fixed identity colors (project palette hexes, the gray family) are the only allowed literals.
- Terminal/trace surfaces (verification logs) stay dark in **both** themes — terminals are dark.

Mockup boilerplate (put the first part in `<head>`, before any CSS paints):

```js
var root = document.documentElement, KEY = 'sos-os-theme', OLD = 'sos-torque-theme';
function readPref(){ try {
  var v = localStorage.getItem(KEY); if (v==='dark'||v==='light'||v==='system') return v;
  var o = localStorage.getItem(OLD); if (o==='dark'||o==='light') return o;
} catch(e){} return 'system'; }
function resolve(p){ return p==='system' ? (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark') : p; }
root.dataset.theme = resolve(readPref());
window.setThemePref = function(p){             // wired to the dark · light · system select
  try { localStorage.setItem(KEY, p); } catch(e){}
  root.dataset.theme = resolve(p); syncThemeSelect();
};
matchMedia('(prefers-color-scheme: light)').addEventListener('change', function(){
  if (readPref()==='system') root.dataset.theme = resolve('system');
});
```

---

## 4 · Typography

- **Inter** for everything; **JetBrains Mono** for IDs (`NEU-001`), Harvest entry numbers, client codes, terminal traces, and rank numbers.
- Scale (px, **SpannerOS edit mode; present = ×1.125** — see §12): page title **26/800**, panel heading **17–20/800**, big number **40/800**, body **16/400**, data **15.5/400–600**, small **15**, section/axis labels **12.5/800 with 0.08em letter-spacing** (these small caps-feel labels are written in CAPS — the one place caps are used), chart labels **11**. In a KPI tile the unit (h, $) is not muted: it takes the same ink as its number. The old 13–14.5 body scale survives only on the June `-unbound` reference pages.
- `font-variant-numeric: tabular-nums` on **every** numeric surface (tables, stats, day cells).
- `-webkit-font-smoothing: antialiased` on body. Negative letter-spacing (−0.01 to −0.02em) only on titles ≥21px.

---

## 5 · Surfaces & layout

- **Top bar — the header is navy in every skin and both themes** (DR-55, DR-73; Mason's standing rule 2026-10-05). Background `var(--hdr-bg)` (`#293A49`; `#1D2B37` in dark, so it stays distinct from the page), white text, no blur and no bottom hairline. 66 px tall; sticky, and its height is measured, never hardcoded. Controls on the bar (audience indicator, week stepper, $ ⇄ h, segments, buttons, selects; theme and viewing as sit in the dock account menu, R-05) use the `--hdr-*` tokens: `--hdr-ctl` fill, `--hdr-line` border, `--hdr-tx` text; a selected segment is `--hdr-on-bg` light azure with navy `--hdr-on-tx` text (white on azure fails 4.5:1). Contrast checked for these exact values: text ≥ 4.5:1, UI ≥ 3:1. Contains the lockup, then the controls right-aligned via a `flex:1` spacer. **No logo SVG on Torque pages.** One row at ≥1100 px.
- **Header lockup — RATIFIED 2026-10-06 (Q-174, option B of `mockups/wordmark-spanner-os-options.html`; supersedes C26-18).** One treatment on the shell, sign-in and the planning skin's bar:

  ```html
  <span class="brand">spanner <i>os</i><span class="bsep"></span><span class="btitle"><span class="pre">section<span class="psep"></span></span><b>page name</b></span></span>
  ```
  ```css
  .tbar .brand{font-family:'SpannerSans','Inter',sans-serif;display:block;white-space:nowrap;
               font-size:42.4px;font-weight:400;line-height:1;color:var(--hdr-tx);}
  .tbar .brand > *, .tbar .brand .btitle > *{vertical-align:baseline;}
  .tbar .brand i{font-style:normal;color:var(--hdr-accent);}            /* the "os" */
  .tbar .brand .btitle{display:inline;font-family:'Inter',system-ui,sans-serif;font-size:22px;
                       font-weight:400;letter-spacing:.04em;color:var(--hdr-tx);}
  .tbar .brand .bsep, .tbar .brand .psep{display:inline-block;width:0;height:28px;
       border-left:1px solid var(--hdr-accent);margin:0 24px -2.9px;}
  .tbar .brand .psep{margin:0 20px -2.9px;}
  @media (max-width:620px){                                             /* the same lockup at 0.7 */
    .tbar .brand{font-size:29.7px;overflow:hidden;text-overflow:ellipsis;}
    .tbar .brand .btitle{font-size:17px;}
    .tbar .brand .bsep, .tbar .brand .psep{height:19.6px;margin:0 14px -2px;}
  }
  ```
  Rules:
  - The wordmark is **"spanner os"**: lowercase, a space, then "os" in azure, all SpannerSans Regular at **42.4 px**. SpannerSans has the logo's proportions (letters 52.4 / descender 18.4 per 100 px), so 42.4 px gives the brand guidelines' header wordmark: **30 px of ink, 22.2 px letters**, the same as the s07 lockup's 30 px SVG. "spanner" itself never changes; "os" is a separate word.
  - The **crumb** after the divider is **Inter 22 px regular, letter-spacing .04em**, the brand header's label style: section prefix, a smaller divider, then the page name. Emphasis is color only. The section prefix stays visible below 1440 px and is dropped only when it does not fit (R-04).
  - **Lockup alignment:** the crumb's dividers sit on one shared baseline with the divider centered on the letter body. In any "spanner | text" lockup, including decks and compare pages, the center of the A aligns to the midpoint of the pipe (R-03).
  - **Dividers** are 28 px tall, 1 px azure **borders** (not 1 px backgrounds, so they snap to whole pixels), centered on the 22.2 px letter body (11.1 px above the baseline, so each bottom sits 2.9 px below it).
  - The wordmark, dividers and crumb are **one line of text on a shared real baseline**. Never align dividers on an empty flex item's synthesized baseline; that put them too high.
  - Below 620 px the lockup scales to 0.7 (letters 15.5 px), crumb 17 px.
  - Why: Mason raised the header three times (DR-55, DR-73, ER-4). The C26-18 lockup (`spannerOS` 26 px, 13.6 px letters) sat well under the brand's 22.2 px letters, and the crumb inherited SpannerSans.
- **Font embedding:** SpannerSans is embedded per page as a woff2 data URI (`@font-face` + `src:url(data:font/woff2;base64,…)`) — 4.3KB file at `Mason-Claude/Projects/Brand/spanner-sans/SpannerSans-Regular.woff2` (full basic-latin, 98 glyphs), ~5.7KB embedded; offline/portal-cached, no network fetch. Study + provenance: `torque-header-study.html`.
- **Sticky sub-strips** (stat constellations) are blurred glass: `backdrop-filter: blur(18px)`, background `color-mix(in srgb, var(--bg) 78%, transparent)`, 1px bottom hairline. (The top bar used this treatment until the navy header, 2026-10-05.) **Never hardcode sticky offsets — measure the bar's `offsetHeight` at runtime** (and re-measure on resize / use ResizeObserver). Same rule for chart geometry: measure rendered columns, never assume widths.
- **Panels:** 16px radius, 1px `var(--line)` border, `var(--panel)` fill, `var(--shadow)` (light) / nothing-or-glow (dark). Padding 13–17px. Panel title = the small caps label, with inline explanatory text in `var(--mut)` after it.
- **Page width:** **use the whole window** (R-20, decided 2026-10-22; DR-2 superseded 2026-09-30, see §12). No max-width on SpannerOS meeting screens, but leave space where possible and accept density where a screen needs it. Panels flow into auto-fit columns (min 520px), tables size to content, spare width goes to weeks, charts or the comment rail. 24px side padding (16px on phone). Grids: CSS grid with 16px gaps. Documents and portal pages keep a max-width.
- **Inputs:** `var(--inbg)` fill, 9–10px radius, 1px line border; focus = azure border, no outline ring. Inline hints use a 2.5px azure left border on an `--inbg` strip.
- Azure focus/selection glow: `box-shadow: 0 0 16–24px rgba(6,166,237,0.12–0.18)` plus azure border.

---

## 6 · Components

- **Buttons.** Primary: azure fill, white 800 text, 11px radius, `box-shadow: 0 4px 22px rgba(6,166,237,0.3)`; hover = `filter: brightness(1.07)`. Ghost: 1px line border, muted text. Acknowledge/warning action: orange fill. Pill actions (nudges): 999px radius, azure-tinted fill + border.
- **Chips & pills:** 999px radius; status colors as 12% tint background + 35% tint border + colored text (`color-mix` does the tints). States: pending=orange, approved/ok=green tint, drifted=solid orange + white text.
- **Segmented controls:** pill group on `--inbg`/panel, 2px padding, **selected segment = light fill, 2px ink ring, bold text (R-108, 2026-11-03; was an azure fill)**. A segmented row replaces a dropdown for a short list (R-80).
- **Tables:** hairline rows only (`--line`), 10px caps headers in `--dim` aligned with their data, right-aligned numerics, hover row = 5% azure tint. Sortable headers show a faint arrow at rest, the active one heavier with its rank (R-70, R-72). Sticky first column uses opaque `var(--stick)`.
- **Avatars:** rounded-square (9–12px radius), azure 14% tint fill + 30% tint border, azure initials. Variants: amber tint = expense rows, orange tint = pending/placeholder.
- **Decision buttons: accept / decline always offers Change** (Mason, 2026-10-07). Wherever a person can accept or decline, or anything equivalent (approve / decline, request / not now, open / not yet, sign off / reject), a **Change** button sits between them, in the order primary · Change · negative, e.g. "Approve · Change to… · Decline", "Request 5 h · Change hours… · Not now". Change opens the same item pre-filled; submitting it counts as the decision (recorded as changed). A plain Done or dismiss on an information-only item doesn't need it.
- **Steppers & rails** (guided flows): numbered circles — done = azure fill + white check, current = azure border + glow, todo = line border; clickable; pair with a progress ring (`stroke-dasharray` arc) in the bar.
- **Flags:** glass card, orange border (info variant: line border + azure icon), round icon chip, body in `--mut` with `--tx` bolds.
- **Day/grid cells:** rounded 7–10px tinted cells — azure 16% = at-target, orange 18% = surge band; hours over plan are the program's plain solid hue running past its lighter plan bar, with no stripe, outline or orange slice, and over-plan numbers keep orange text (2026-11-02, see §12); a real 0 shows as 0 and an em-dash in faded `--dim` means not set.
- **Terminal trace:** JetBrains Mono 11px on near-black glass with azure border tint; lines fade-translate in, staggered ~260–280ms; ✓ green, ⚠ orange, ▸ headers azure.
- **Persistent comment bar / command bar:** fixed bottom, blurred like the sticky sub-strips; body gets matching `padding-bottom`.

---

## 7 · Charts

- **Hand-rolled inline SVG only** — no chart libraries (alignment + theming control; same rationale as the planner grid decision).
- **Series semantics (fixed):** actual = `var(--azure)` (solid, heaviest 2.4–2.6 stroke, area fill at 13–16% tint); estimate, forecast and any planning shading = `var(--est)` gray (R-54); estimate-from-now = `var(--mut)`; baseline = `var(--tx)` dashed at 0.5 opacity; budget/zero reference = `var(--orange)` dashed; gray stepped area = estimate envelope on bar charts.
- Gridlines = `var(--line)` 1px; axis labels = `var(--dim)` 8.5px; key values annotated directly on the chart in series color, 700 weight.
- Week marking: the selected week is a light-blue column on every table and chart, with rule lines for this week and next (R-55). This week and the reviewed week are labeled azure bands behind the plot, at the same x on stacked charts (R-56). The band is azure at 12% in the light theme and 15% in the dark theme, one value for every screen and chart. This replaces the earlier 8% (spec) and 17% (D3) values.
- Approved-actuals rule carries everywhere: the actual series stops at the last approved week with a dot.
- Every mark hovers to a popover with its detail and clicks to open its panel (R-117). Phase rows carry their phase icon (R-118). Compared rows share one scale, keyed in the header; a total row uses its own neutral scale (R-119).
- In-progress bars: azure at 28–38% opacity with 1px azure stroke.
- Tooltips/crosshairs sync across all chart panels on a page (shared hover registry pattern — see interface-9d). Stacked charts share one x-scale and right gutter, and the popup shows estimate minus actual in addition to what it already shows (R-60).

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

- [ ] Token block copied verbatim (Torque + system + header tokens); **default follows the system**; dark · light · system select persisting to `sos-os-theme`, set before first paint
- [ ] Dark page surface is Spanner navy `#293A49`; both themes checked
- [ ] Navy header bar with the "spanner os" 42.4 px lockup, Inter 22 px crumb, border dividers on a shared baseline
- [ ] Every accept / decline offers Change, in the order primary · Change · negative
- [ ] All SVG colors via `style="...var(--x)"` (toggle restyles charts with no re-render)
- [ ] Sticky offsets measured, not hardcoded
- [ ] Numbers in tabular-nums; a real 0 shows as 0, em-dash only for not set
- [ ] Color = meaning audit: nothing azure that isn't interactive/actual, nothing orange that isn't a warning, nothing amber that isn't watch, estimate and forecast gray
- [ ] Money gated on member-visible surfaces
- [ ] Footer: design-exploration note + functional reference
- [ ] JS syntax-checked; every `getElementById` target exists

---

## 11 · Relationship to other Spanner standards

| Surface | Standard |
|---|---|
| SpannerOS app screens, internal tools, interactive mockups | **Torque** (this skill) |
| How SpannerOS screens are assembled (modes, shell, money gating, components) | `spanneros-design-system` skill / `specs/spanneros-design-system.md` |
| Documents, decks, PDFs, reports, one-pagers | `spanner-brand-visual` (s07 lockup, 120% type scale) |
| Plan/notes infographic pages, portal article pages | `spanner-brand-visual` |
| Data series & project identity colors (everywhere) | `spanner-data-palette.html` (shared by both) |

History: Torque began as the "unbound" exploration (June 11, 2026, weekly-review variants). The 14 reference pages keep their `-unbound` filenames; the language itself is named Torque.

---

## 12 · Change log

- **2026-11-04 — Nov 4 walk-through rules R-117 to R-128 (Mason, seven reviews of `mockups/261104-walkthrough-feedback.html`).** Rule text is in the design-system spec §12. What changes in Torque: §7 charts gain hover popovers on every mark and click-to-open (R-117), phase icons on phase rows (R-118), one shared scale for compared rows with the key in the header and a neutral total scale (R-119); §6 components gain the segmented progress bar on blocks (R-121), checklist evidence rows (R-122), in-place Claude proposals (dashed azure, R-123), the selected-day outline and amber "Not today" note (R-124), and side-panel editors that replace the panel in place (R-128). Estimate-and-actual pairs (R-116) now also draw in the time grid's week column. Not built yet.

- **2026-11-03 — design review answers; R-94 to R-116 written in (Mason, interface-98 review).** Rule text for R-94 to R-107 is in `specs/261029-design-rules-from-exec-review-build.md` and now also in the design-system spec §11; R-108 to R-116 are new and listed there too. What changes in Torque:
  - **Selected state is neutral (R-108).** §6 segmented controls: light gray fill, 2 px ink ring, bold text. No azure fill. Supersedes "active segment = azure fill white text". Check on a projector in present mode; dark theme needs its own pair (light segment, navy text), as the header controls already do.
  - **Primary button stays azure #06A6ED (R-109, Mason: "keep that azure instead of dark").** No change to the §6 button spec. Known cost, not fixed: white on this azure is 2.73 to 1 (3e). Navy text would be 4.28 to 1, still under 4.5. One primary button per screen, only where an action saves something.
  - **Links are blue and underlined (R-110).** Deeper blue `#0A7DB8` (4.53 to 1 on white; `--azure-ink`, `#5CC6F7` in dark), never the bright azure and never in fine print.
  - **Units in the header (R-111), editable cells look editable (R-112), a program page names its program (R-113), quiet states (R-114):** inside a signal table on track and "not set" are plain and only watch and at risk get tinted pills; a program list or scan row shows a status pill on every row with no row tint.
  - **R-103 changed from dot to pill:** a program list shows the program color as a bar and the verdict as a pill (on track, watch, at risk); no row tint, no left bar.
  - **Controls stay put (R-115)** and **estimate and actual are a pair (R-116):** the wider, lighter estimate bar sits behind the narrower solid actual bar, same program color, for the selected week; a future week shows the estimate only; no hatching, hours past plan just run longer. The §5 time-grid week bar is unchanged (Mason, Nov 3, second pass).
  - **Agrees with the 2026-11-02 entry:** hours past plan lose their stripes (PR #380), so R-116 and the desktop program bar now match. Check the app's program bar uses the same behind-and-on-top layout when 5c is built.
  - Settled in the same review: "five bands" keeps its name; a first-visit strip plus legend on the time grid; right-click opens W4 and long-press does the same on touch; my week goes to any week the forecast covers. Mockup: `mockups/interface-98-design-feedback-before-after-261030.html`.
  - **Built 2026-11-03 (Claude Code), in review, not merged:** PRs #392 (tokens, neutral selected state, `--link`, status pill), #393 (exec review), #394 (time grid), #395 (D3 pairs, flip, right-click), #396 (my week), stacked in that order. The navy header bar and the brand skin keep their own selected states, as the handoff asked (the design-system table says "same" for brand; Mason to decide). Not built: D3 notes per person per program (no store for them; needs a decision). The desktop program bar from PR #380 already uses the behind-and-on-top layout.

- **2026-11-02 — over plan loses its stripes (Mason, Nov 2 TPL sync; PR #380).** In a bar, each program's plan is its hue lighter and wider behind, logged is the same hue solid and narrower on top, and hours past the plan are just more solid hue: no diagonal ink stripe (Q-192, R-52's bar half) and no orange outline. Orange stays on the numbers. Applied on the desktop time page (`.ovp` is now plain solid) and shown on A8 ("plan and logged in a bar"). The design-system mockup (`design/mockup-src/ds/`) never drew the stripe, so it has nothing to change. Reasoning: `modules/design-system.md`.
- **2026-10-23 — design rules approved from Mason's review (R-n = `specs/261022-design-rules-from-feedback.md`).** Decided 2026-10-22: **estimate and forecast are gray, not amber** (R-54: §1, §2, §7; amber now means watch only); **the default theme follows the system** (R-67: §2, §3; replaces dark default); **whole window with space** (R-20: §5). Approved: section prefix stays visible below 1440 px, may be dropped if it does not fit (R-04, §5); account controls in the bottom-left dock (R-05, §3, §5); lockup alignment (R-03, §5); selected-week column and labeled this-week / reviewed-week bands, azure 12% light / 15% dark (R-55, R-56, §7); over plan is a hatch of the program hue, orange text for numbers (R-52, §6); popup shows estimate minus actual in addition (R-60, §7); sort cues and default order (R-70, R-71, R-72, §6); real 0 shows as 0 (R-33, §6, §10, replacing the em-dash-never-0 line); native controls follow the theme (R-68, §3). The layout, wording, week, sort and name rules are in `spanneros-design-system.md` (§2, §4–§7). The deck rules R-90 (one slide background) and R-92 (16:9) were approved and belong to the brand skill, not here. The installed `torque-design-language` skill copy predates this entry.
  - **Pending (not yet rules):** R-35 (pare generated pages to the exec summary), R-48 (section headers larger than the biggest text in their box), R-91 (no bolder-than-bold type): held. R-61 (type-size floors; axis 8.5 px, table headers 10 px vs 12.5 px labels above) and R-62 (amber contrast; amber text 2.6 to 3.2 in light) wait for comparison examples. R-93 (client-facing output: brand skin vs SpannerOS style) waits for options and a team decision. R-13 (explicit close on inline panels) waits for an example. Also open: the estimate gray's value and distinct treatment, (the week-marking tint is now settled: 12% light, 15% dark). KPI tile units are no longer muted: the unit (h, $) takes the same ink as its number, not a muted gray (§4, §6).
- **2026-10-15 — stat band (SY-24, Torence).** A stat row over a table sits on its own tinted band, or is offset; it is never lined up one-to-one with the table's columns, where figures read as headers. Rule text is in the design-system spec §6 and §10.
- **2026-10-13 — program color map (ER-123, ER-142; commit fbe7de4).** A program is one color on every screen, read from one shared map, launch dates included for Tin. Rule text is in the design-system spec §5.
- **2026-10-07 — specs brought up to the latest decisions (Cowork).** §2 now states dark as the default and carries the system and header tokens; §3 rewritten for the three-way theme choice; §5 header and lockup replaced; §6 gains the Change rule; §10 checklist updated. The installed `torque-design-language` skill copy predates this entry.
- **2026-10-07 — dark is the default theme (Mason; PR #113).** Everywhere: shell, sign-in, /planning, time entry. Each person picks dark, light or system (a three-way select), remembered under one key, `sos-os-theme` (`lib/theme-pref.ts`); the old `sos-torque-theme` is read as a fallback. Supersedes "light is the default" in §2 and §3.
- **2026-10-07 — every accept / decline offers Change (Mason).** §6. Recorded in `modules/design-system.md`.
- **2026-10-06 — header lockup "spanner os" (Mason, Q-174, option B; PRs #108, #109).** SpannerSans 42.4 px (the brand header wordmark's 30 px ink, 22.2 px letters), "os" azure, crumb Inter 22 px regular, 28 px azure border dividers centered on the letters, one shared baseline, 0.7 below 620 px. Supersedes the C26-18 `spannerOS` 26 px lockup in §5.
- **2026-10-05 — the header bar is navy in every skin and both themes (DR-55, DR-73; Mason).** `--hdr-*` tokens; `#1D2B37` in dark. Supersedes the blurred page-colored top bar in §5.
- **2026-10-01 — header crumb (Mason):** the top bar's section and page name now use the screen title's font (Inter), regular weight, at the brand header's 22px with its .04em tracking, keeping the section crumb, instead of 18px SpannerSans. The wordmark is unchanged. Applied in `design/mockup-src/ds/part1.css`; every desktop mockup rebuilt.
- **2026-09-30 — SpannerOS design system rev 1** (`specs/spanneros-design-system.md`, reference page `mockups/spanneros-design-system.html`). Changed here rather than forked:
  - §4 type scale raised to 16px body / 15px small (Mason's standing preference), with a present-mode factor of 1.125 (`--s`). One layout, two type sizes (DR-1).
  - §5 page width: no max-width on meeting screens (DR-2).
  - Added system tokens alongside §2 (not replacing it): spacing on a 4px base, radii (`--r-panel 16 · --r-btn 11 · --r-in 10 · --r-cell 8 · --r-chip 999`), three elevation levels (`--e1` = `--shadow`, `--e2` popover), and the type-scale variables.
  - The brand skin is formalized as token overrides on the same names (`html[data-skin="brand"]`), not a second system — see the skin table in the design-system spec §8.
  - **Ratified 2026-09-30 (Q-050):** the generic project hues reordered (orange · plum · olive · rose · green · violet · sienna · amber · berry), the Tin ramp revised (midnight `#073D5C` retired, cornflower `#4F93C4` added, assigned by launch alternating light/dark), and a lighter "grid tone" for capacity fills (DR-9). §2's reference to the Tin blue ramp now means this ramp.
  - The installed `torque-design-language` skill copy predates this entry; this file is the source of truth.
  - 2026-09-30 (later): **present mode retired** (Q-053). One layout, one type scale (`--s` = 1). Restricted-note masking survives as a per-session "hide restricted" toggle.
  - 2026-09-30 (review 3): **present mode kept** after all (DR-72, reverses the retirement above). Present is read-only with collapsed required strips as well as ×1.125; prep is renamed edit.
