---
name: spanneros-design-system
description: Rules for designing, building or reviewing any SpannerOS screen, mockup or component: layout, edit/present modes, shell, money gating, field states, palette, components, charts, skins, phone.
---

# SpannerOS design system

This skill covers how SpannerOS screens are put together: one layout with edit and present modes, the shell, money gating, field states, names, color, components, charts, the brand skin and the phone surface. It sits on top of **Torque**, the visual language (tokens, glass panels, type). Use it for any SpannerOS work, including the app (`spanner-planner`), HTML mockups, portal tools that live inside SpannerOS, and Arne's Forge (BD) build.

**Don't use it for** client-facing collateral, decks, documents, proposals or marketing pages. Those follow `spanner-brand-visual` and `spanner-brand-voice`. The one exception is a SpannerOS screen a client signs in to see, which uses this system's **brand skin** (§9).

_Snapshot of the rules as of 2026-11-04 (design system rev 1, IA rev 1, phone rev 1, the rule list approved 2026-10-23, R-94 to R-116 approved 2026-11-03, R-117 to R-128 approved 2026-11-04, and the 2026-11-02 color decisions; rule ids R-nn up to R-93 are from `specs/261022-design-rules-from-feedback.md`, later ones from `specs/spanneros-design-system.md` §11–§12)._

---

## 0 · Sources of truth, and when they beat this skill

This skill is a snapshot, and the written specs win over it. When you can reach the files, read the one that fits before building anything. Paths are relative to `_SpannerClaude/ClaudeFolders/Mason-Claude/Projects/SpannerOS/`.

| Topic | Source of truth |
|---|---|
| How screens are assembled | `specs/spanneros-design-system.md` |
| Tokens, glass, type, header, theme, charts | `specs/torque-design-language.md` (change log is §12) |
| The reasoning behind decisions made after rev 1 | `modules/design-system.md` |
| Where a screen lives: sections, routes, roles × screens | `specs/spanneros-ui-architecture.md` |
| Phone and watch | `specs/spanneros-phone-design-system.md` |
| Member and contractor surfaces | `reference/member-surface-ui-rules.md` |
| Layout and interaction requirements (DR-n) | `specs/260930-ui-design-review-requirements.md` |
| Living references | `mockups/spanneros-design-system.html` · the app's `/admin/design-system` (A8) |

**Code (`~/Developer/spanner-planner`).** `app/(os)/torque.css` holds the tokens and components, ported verbatim from the mockup. `app/(os)/shell.css` holds the header lockup. `lib/palette.ts` holds the project colors, `lib/theme-pref.ts` the theme choice, `lib/er.ts` the on-the-rails verdict, `lib/money*.ts` the money gate, and `app/(os)/_components/` the shared parts (`chip`, `kpi`, `step-head`, `week-stepper`, `comment-rail`, `seg`, `record`, `page-skeleton`).

Three rules about the sources:

- **There is one rule set, not two.** Never fork a second spec. A change goes into the spec and gets logged in Torque §12, and then the mockup source and `torque.css` change to match.
- **When sources disagree, the newer dated decision wins.** The specs were brought up to date on 2026-10-23.
- **If a rule here conflicts with what you find, say so to the user.** Don't silently pick one.

---

## 1 · Which system for which job

| Surface | System |
|---|---|
| SpannerOS app screens, internal tools, interactive mockups | **This skill + Torque** |
| A SpannerOS screen a client signs in to (budget report, client portal) | This skill, **brand skin** |
| Phone screens | This skill + §11 (the phone spec) |
| Decks, documents, PDFs, reports, one-pagers, marketing pages, plan/notes status pages | `spanner-brand-visual` |
| Chart and project colors, everywhere | The data palette (§6) |

---

## 2 · Tokens

The root element carries four attributes:

- `data-os`: scopes every selector; the app's `AppShell` sets it.
- `data-theme`: `dark` or `light`.
- `data-skin`: `torque` or `brand`.
- `data-mode`: `edit` or `present`.

In a standalone mockup, `:root` / `html[data-theme=…]` is fine. In the app, every selector is `html[data-os]…` so it can't restyle the old planner routes.

```css
/* Torque — dark */
html[data-theme="dark"]{
  --bg:#293A49; --bgglow1:rgba(6,166,237,.10); --bgglow2:rgba(226,103,42,.05);
  --panel:rgba(255,255,255,.045); --panel2:rgba(255,255,255,.075); --line:rgba(255,255,255,.10);
  --tx:#E8EEF4; --mut:#93A3B2; --dim:#5E6E7D;
  --azure:#1FB2F5; --orange:#ED7A40; --amber:#F6B511; --green:#2EC592; --lblue:#CAECF6;
  --shadow:none; --glow:0 0 36px rgba(6,166,237,.07); --inbg:rgba(0,0,0,.25); --stick:#314254;
  --e2:0 0 0 1px rgba(255,255,255,.08),0 18px 48px rgba(0,0,0,.35);
  --hdr-bg:#1D2B37;
}
/* Torque — light */
html[data-theme="light"]{
  --bg:#F4F7F9; --bgglow1:rgba(6,166,237,.06); --bgglow2:rgba(226,103,42,.03);
  --panel:#FFFFFF; --panel2:#FFFFFF; --line:#DCE3E8;
  --tx:#293A49; --mut:#6B7A8A; --dim:#97A2AC;
  --azure:#06A6ED; --orange:#E2672A; --amber:#F6B511; --green:#0B7C58; --lblue:#CAECF6;
  --shadow:0 1px 3px rgba(41,58,73,.08),0 8px 28px rgba(41,58,73,.05);
  --glow:var(--shadow); --inbg:#F4F7F9; --stick:#FFFFFF;
}
/* System tokens (both themes) */
:root{
  --r-panel:16px; --r-in:10px; --r-btn:11px; --r-chip:999px; --r-cell:8px;
  --sp1:4px; --sp2:8px; --sp3:12px; --sp4:16px; --sp5:20px; --sp6:24px; --sp8:32px; --sp10:40px;
  --navw:232px; --navw-c:64px; --railw:320px;
  --s:1;  /* edit = 1, present = 1.125 */
  --fs-title:calc(26px*var(--s)); --fs-h2:calc(20px*var(--s)); --fs-body:calc(16px*var(--s));
  --fs-data:calc(15.5px*var(--s)); --fs-small:calc(15px*var(--s)); --fs-cap:calc(12.5px*var(--s));
  --fs-chart:calc(11px*var(--s)); --fs-big:calc(40px*var(--s));
  --gray-dto:#B9C1C8; --gray-nb:#97A2AC; --gray-ooo:#76828D; --gray-leave:#55606B;
  --red-alert:#D94040;
  --est:#8A97A4;  /* estimate gray (R-54), defined here for every screen, no amber fallback; dark #A7B3BF */
  --e1:var(--shadow); --e2:0 2px 6px rgba(41,58,73,.10),0 16px 40px rgba(41,58,73,.10);
  /* header bar: navy in every skin and both themes */
  --hdr-bg:#293A49; --hdr-tx:#FFFFFF; --hdr-accent:#06A6ED; --hdr-link:#8FD6F7;
  --hdr-ctl:rgba(255,255,255,.06); --hdr-line:rgba(255,255,255,.45);
  --hdr-on-bg:#8FD6F7; --hdr-on-tx:#1D2B37;
}
html[data-mode="present"]{ --s:1.125; }
```

The page background is always two radial glows over `--bg`:
`radial-gradient(1100px 500px at 75% -10%, var(--bgglow1), transparent 60%), radial-gradient(800px 420px at 8% 8%, var(--bgglow2), transparent 55%), var(--bg)`.

**Fonts.**

- **Inter** for everything.
- **JetBrains Mono** for IDs, Harvest entry numbers, client codes and terminal traces.
- **SpannerSans** only for the wordmark. In a mockup, embed it as a base64 woff2 data URI (about 5.7 KB). The source file is `Mason-Claude/Projects/Brand/spanner-sans/SpannerSans-Regular.woff2`.
- Use `font-variant-numeric: tabular-nums` on every numeric surface.

**Theme.**

- **The default theme follows the system setting** (R-67; Mason, 2026-10-22). A person with no stored choice gets light or dark from `prefers-color-scheme`.
- Each person can pick dark, light or system. That is a three-way select, not a toggle, remembered in local storage under `sos-os-theme`. The old key `sos-torque-theme` is read as a fallback.
- A pre-paint script sets the theme before the first frame, and its fallback is `system`, not `dark`. It repeats `lib/theme-pref.ts`.
- Every surface is checked in both themes, and a light-theme check is part of the checklist (§12). Chart colors reference CSS variables.
- Form fields use theme colors, and native controls get a matching `color-scheme` (R-68).

---

## 3 · One layout, two modes: edit and present

Every screen has **one layout** (DR-1) and two modes, in one component tree with `data-mode` on the root. **The mode lives in the URL (`?mode=present`), never in storage.** Someone would leave a stored toggle on and mistake a mask for an omission.

| | edit | present |
|---|---|---|
| type factor `--s` | 1 | 1.125 |
| body · data · small · label | 16 · 15.5 · 15 · 12.5 px | 18 · 17.4 · 16.9 · 14.1 px |
| big number · page title | 40 · 26 px | 45 · 29 px |
| forecast cells | editable, outlined, autosave (roles that may edit) | read-only |
| required human fields | text box, save, "none this period" | one strip: "required — not entered" |
| comment rail | threads + composer | threads only |
| what-if | start, discard, promote | shown if running |
| restricted fields | shown to those allowed | hatched "restricted" chip |
| data-check fixes | fix buttons | count only |

Present must look **different, not just bigger**: the edit chrome goes. Interface-27 (the program page) is the model. "Prep" is the old name for edit; don't use it.

---

## 4 · The shell

### 4.1 Sections and navigation

- **Six sections, in lifecycle order:** home · **Forge** (pipeline & launch) · **Workbench** (programs) · **Drivetrain** (studio) · **Ledger** (business) · admin.
- `/` sends each role to its own home.
- **A view is fully described by its URL**: `week`, `mode`, `half`, `unit`, `step`, `tab`, `by`. Old routes 308-redirect.
- **The side nav shows each role only the screens it can open.** It never lists a screen and then says "No access". The Director sees everything. Routes and the role × screen matrix are in the IA spec.
- **Side nav breakpoints:** ≥1280 px expanded and collapsible (collapse is a per-person local-storage convenience); 900–1279 px icons only, opens on tap; <900 px off-canvas behind ☰. It reaches every section, is sticky at full height, and its collapse control is always on screen, also when collapsed to icons (R-06).
- **Account dock (R-05).** Whole-screen controls (viewing as, theme and the like) live in one account menu in the bottom-left dock of the side nav, not in the top bar. One sidebar show/hide icon sits in the top-bar tab row.

### 4.2 Top bar

- **The bar is navy with white text in every skin and both themes.** It is `#293A49`, or `#1D2B37` in dark so it still reads as a bar. It is 66 px tall.
- **Controls on the bar** use the `--hdr-*` tokens. A selected segment is light azure with navy text, because white on azure fails 4.5:1.
- It holds only what the screen as a whole needs, and the account-level controls moved to the dock (R-05):
  - lockup and crumb
  - audience indicator
  - week stepper
  - $ ⇄ h
- It fits on one row at ≥1100 px.
- **Controls sit next to what they change** (R-07, DR-6): chart controls on the chart, row controls on the row, sort in the card header. A control may sit inside the box it changes when that makes sense and fits.
- **The same control is in the same spot on every screen** (R-08). The week stepper does not move between clicks, "return to this week" sits above the pill (left end when ahead), and an offset chip shows -1, +2.
- **Controls stay clear of the comments edge tab** (R-09): week stepper and show/hide controls move left, with 64 px right padding at ≥1280.
- **The program head is steady** (R-10): fixed rows, and tabs do not shift it.
- **Header lockup** (Mason, 2026-10-06; exact CSS in Torque §5):
  - The wordmark is **"spanner os"**: lowercase, with a space, and "os" in azure. It is SpannerSans at **42.4 px**, which gives the brand's 30 px of ink and 22.2 px letters. "spanner" itself never changes.
  - The **crumb** after the divider is Inter 22 px regular, letter-spacing .04em.
  - **Dividers** are 28 px, 1 px azure *borders* centered on the letter body. Never draw them as 1 px backgrounds, and never align them on an empty flex item's synthesized baseline.
  - Everything sits on one shared text baseline, and the divider is centered on the letter body (R-03). For any "spanner | text" lockup, including decks and pages, the center of the "A" lines up with the midpoint of the pipe. Below 620 px the lockup scales to 0.7.
  - **The section prefix stays visible below 1440 px** (R-04). If the section name does not fit, it may be dropped.
  - Don't put a logo SVG on Torque pages.
- **"Viewing as"** previews another role's *layout* with the admin's own data and permissions. It lives in a cookie and is never in a URL.

### 4.3 Comment rail, width and sticky elements

- **The comment rail** sits on the right of every meeting screen (DR-3): a summary block, the scope chips (week · program), threads, and the composer in edit. It is 320 px docked (360 at ≥2200) and becomes a drawer below 1280. Last week's note shows, labeled, but never counts, and the "why" is required (R-22).
  - It is collapsible with a "comments" edge tab, and its width is adjustable by dragging its left edge, remembered per viewer (R-23).
  - Every note or comment field says who can read it (R-24).
  - Optional note fields are plain optional fields, with no orange "required" strip (R-25).
- **Use the whole window** (R-20, DR-2; decided 2026-10-22).
  - No max-width on meeting screens. Panels flow into auto-fit columns: min 520 px, wide panels 700 px.
  - Tables size to their content. Spare width goes to charts or more weeks, never to empty gutters, and there is no sideways page scroll at laptop width.
  - Leave space where possible. Density is fine where a screen needs it.
  - Side padding is 24 px (16 on a phone).
  - Documents and portal articles keep a max-width.
- **Wide tables** pin identity columns left and the note column right, and only the week columns scroll. A copy of the header floats on scroll (R-21).
- **Stat rows and KPI tiles.** A stat row over a table sits on its own tinted band, or is offset. It is never lined up one-to-one over the table's columns (R-26). KPI tiles each have their own bordered tile (R-27). Big numbers in a row share a baseline (R-28).
- **Text.** Truncate names with an ellipsis, and a name never runs into the next column or date (R-29). Text areas grow with their text, have horizontal padding and show the full placeholder, and notes columns are wider, resizable and auto-height (R-30). Never discard unsaved text in one field when saving another (R-31). Show hours with no more decimals than needed, two places for .25 and .75 (R-32).
- **Measure sticky offsets** from the bar with a ResizeObserver. Never hardcode them. Measure chart geometry the same way. Group and column headings stay sticky while their columns are on screen (R-77).
- **Loading and feedback.** Every section route has a loading skeleton, and a view switch gives feedback at once: the control lights, the page dims, a progress bar runs, neighboring weeks prefetch (R-11). Keep scroll position when switching a filter or segment (R-12).

---

## 5 · Money, names and field states

### 5.1 Money gating

- `moneyOK = role allows money AND the audience isn't part 1`.
- **Members and contractors see hours only:** no rates, $, budgets or EAC anywhere. **Cost rate and margin** are a separate finance tier (Director, finance).
- **The Monday meeting:** part 1 (full team) is hours only, and part 2 (TPLs) is $ + h. A marker in the step rail flips the audience, and money follows by itself.
- **When $ isn't allowed:** the $ segment is disabled and says why (the role, or part 1). A screen **never** shows hours under a $ label, a blank, or $0 where a rate would be. It shows **"restricted"**.
- **A Slack draft follows the channel's audience,** not the poster's role. #eng-ops-dashboard is hours only; #finance-tpl may carry $.
- **A client** sees only their own shared programs, at bill rate, for TPL-reviewed weeks. They never see cost rates, margin, verdicts, whys, comments, codenames or other clients.
- **No $ on a phone lock screen,** for anyone.
- **The database enforces money** (security-definer functions, `can_see_project()`), not the UI. Mockups state the gate in the footer.

### 5.2 Names

- Use short names on every internal screen (the accepted short-name table, `lib/short-name.ts`).
- IDs appear in tooltips and setup only, in JetBrains Mono.
- The full "client | project" name is for client-facing output.
- Write **"TPL"**, never "lead". Apple programs are always **"Tin"** (codenames on every screen, R-41).
- A first-name-only display really shortens the row, and columns are resizable (R-42).
- **Name actions after the destination in plain words** ("mark approved", "add to the total", "submit the week"). A control names its action, not its state (R-43).
- **No build notes or internal provenance in UI copy.** Status copy stays truthful (R-44).
- **Explain every color, tint or legend entry** (R-45). Counters are unambiguous: "N open" with "X of Y answered", never a countdown that reads as done (R-46).
- **Every record reference** (expense, invoice, deliverable, step, person, program) links to that record (R-49).

### 5.3 Field states

A human field has three states, never two, and "restricted" is not "empty":

- **entered**
- **required — not entered**: an orange dashed strip, counted in a header meter
- **restricted**: a neutral hatched chip saying content exists

Never render a bare blank. Elsewhere:

- **0 renders as 0.** "—" means only "not set" (R-33).
- **"None this period"** is a real state on every required typed field (R-34).
- **"no actuals"** is for a *suspected data gap* only. A real zero is an ordinary under-gap with a why.

---

## 6 · Color

**Color is information, never decoration.** If a color doesn't carry one of these meanings, it doesn't appear.

| Meaning | Color |
|---|---|
| actual · interactive | azure |
| warning · over | orange |
| estimate · forecast · planning | estimate gray (`--est`) |
| confirmed · on target | green (azure on the brand skin) |
| time away · NB · internal | gray family |
| alerts only | red (almost never on a page; **red is never a status**) |

**Estimate gray (R-54, decided 2026-10-22).** The estimate series and any forecast or planning shading is gray on every chart and table. It uses a treatment distinct from the reserved gray family (time away, NB, internal), so it can't be mistaken for them. Never fall back to amber with `var(--est, var(--amber))`; define `--est` globally.

**Status words:** **on track** green · **watch** amber · **at risk** orange.

**Series:**

- **Actual:** azure, heaviest stroke. It stops at the last approved week with a dot.
- **Estimate:** estimate gray. The tolerance band is estimate gray at 14% (±4 h / ±$1k).
- **Baseline and Model:** ink, dashed, at 55%. Baseline reads apart from the estimate even when they are equal.
- **Budget and Surge:** orange, dashed.
- **Selected week (R-55):** a light-blue (azure-tint) column on every table and chart. This week and next get rule lines.
- **This week and the reviewed week (R-56):** labeled bands on every chart, at the same x on stacked charts. The band is azure 12% in light, 15% in dark.
- **One week anchor per screen,** stated once in the header, never two (R-57). Label weeks relatively (last, this, next week) above the date, anchored to the calendar week (R-58). Week groups are separated by thin, low-contrast 1 px vertical lines (R-59).
- **Over plan (2026-11-02, supersedes R-52's hatch):** hours past the plan are the program's own solid hue running past the lighter plan bar behind it. No stripe, pattern, outline or orange slice. Over-plan numbers keep orange text.
- **Estimate and actual in a bar (R-116):** the wider, lighter estimate bar sits behind the narrower solid actual bar, same program color; a future week shows the estimate only. Rows you compare share one scale, keyed in the header; a total row gets its own neutral scale (R-119).
- **Do not color-code a metric** where green is good for the client and bad for Spanner, such as forecast balance (R-63).
- **Person colors** in multi-person charts exclude orange, red and berry (R-53). **Contractors** render differently from staff: a lighter background or a dashed border (R-64). **By-program bars** share one scale, the largest program of the week (R-66).

**Utilization** is three buckets, never collapsed:

- hourly billable: azure
- milestone in-scope: azure hatched
- NB: gray `#97A2AC`

**Time away** is hatched silver in every bar, so it can't read as a gray program.

**Project identity** (`lib/palette.ts`, ratified Q-050). A program is one color on every screen, read from the one shared program color map, including launch dates for Tin (R-50). Nothing computes program colors on its own.

- **Colors are pinned per program (Mason, 2026-11-02; migration 107).** Each program's color is stored in `projects.color_hex` and never re-balances when the active set or the palette changes. A new program takes the first hue in the 12-hue order in `lib/palette.ts` that no active program holds. Only the Director reassigns, on A11 `/admin/program-colors` (previewed on D3's board, logged, one-step undo). Screens read colors through `programColors(…, { themed: true })`. Retired hues stay renderable so stored values still draw.
- **Dark steps:** every hue in the 12-hue order takes its own dark step (CSS `--ph-<hex>` and ink `--phi-<hex>`, generated by `scripts/gen-hue-css.ts`), except rust, which keeps `#B4531A`.
- **Tin owns the blues,** assigned by launch date and alternating light and dark: sky `#6FC6F2` · steel `#2E7FAD` · azure `#06A6ED` · deep `#04679C` · cornflower `#4F93C4`. Midnight is retired. **A Tin segment always carries its label.**
- **The gray family is reserved and never assigned to a client:** DTO/holiday `#B9C1C8` · NB `#97A2AC` · OOO contractor `#76828D` · leave `#55606B`.
- **Plan fills (2026-11-02, Q-275 as revised):** 30% of the program color where a plan sits right against its logged bar (time page, D3 blocks, phone plan block) and 50% where a plan stands alone (D12 future weeks, future week bars). `PLAN_FILL` in `lib/palette.ts`. Charts keep the solid hue.
- More than 8 series in a stacked bar fold to "other".

---

## 7 · Components

Each component has these states. "Money" is the gated variant. Reuse the app's component before writing a new one.

| Component | States | Money |
|---|---|---|
| App shell | nav expanded / collapsed / off-canvas; rail docked / drawer / closed | never |
| Step rail | done · current · todo · owed (orange count); part-2 marker | marker flips money |
| Week stepper | this week (jump disabled) · past approved · past not approved · future; Monday dates; ↩ this week | — |
| $ ⇄ h toggle | h · $ · $ disabled with reason | the gate itself |
| Audience indicator | `mode · audience · $ + h / hours only` | names the gate |
| Comment rail | this week · last week (labeled, not counted) · why (required, orange rule) · pinned to a row | none |
| Expandable row | collapsed · expanded · editing · what-if · approved week locked | Δ$ only in the what-if banner |
| Forecast cell | read · editable · focused · saved ✓ · what-if (amber dashed) · locked (hatched) · this week · error (quarter-hour) · 0 · not set (—) | hours |
| What-if banner | off · on (n changes, Δh, Δ$) · discard · promote | Δ$ only when allowed |
| KPI tile | one number pair, unit in the same ink as the number (not muted), optional meter; warn | cost tile finance-only |
| Stacked bar by program | approved solid · forecast faded; Model/Surge lines | $ or h |
| Actual vs estimate | actual to last approved + dot; estimate; band; gap label | $ or h |
| Signed gap bar | estimate box and actual bar only (no orange over-part, no dashed under-line, ER-71) · on target ↔ · no actuals | $ or h |
| Allocation bar | assigned · open · away (hatched) · over available (plain solid run past the plan) · nothing assigned | none |
| Data-check card | problem · info · fixed; present shows the count | none |
| Approval gate | TPL TRUE → studio manager approves in Harvest → Mason's green light | none |
| Decision buttons | primary · **Change** · negative | Δ$ only when allowed |
| Slack draft | draft · posts after the green light; deep link | follows the channel |
| Chips | on track · watch · at risk · pending · TRUE · drifted · what-if · complete · source (edit only) · basis badge | — |

**Visual specs:**

- **Panels:** 16 px radius, 1 px `--line`, `--panel` fill.
- **Primary button:** azure with white 800 text and a glow. **Ghost button:** line border.
- **Chips:** pills with a 12% tint fill, a 35% tint border and colored text (`color-mix`).
- **Segmented controls:** the selected segment is neutral: light fill, 2 px ink ring, bold text, never an azure fill (R-108). The brand skin keeps solid navy with white text.
- **Links:** blue and underlined, `#0A7DB8` (`#5CC6F7` dark), never the bright azure, never in fine print (R-110).
- **Tables:** hairline rows, right-aligned numerics, an opaque `--stick` first column when sticky.
- **Avatars:** rounded squares with azure-tint initials.
- **Inputs:** `--inbg` fill; focus is an azure border with no outline ring.

---

## 8 · Charts and interaction rules

### 8.1 Charts

- **Use hand-rolled inline SVG only** (no chart libraries). Every color is a CSS variable via `style="fill:var(--azure)"`. Project hexes and the gray family are the only literals. That way the theme toggle restyles charts with no re-render.
- **Axes and legends:** the x axis is Monday dates, thinned to every other label below 46 px per week. Put a one-line legend under the chart and the fuller key in a popover next to it.
- **Stacked charts share one x-scale and right gutter** (R-60). Crosshairs sync across every chart on a page, and the tooltip shows in the hovered chart. The popup shows estimate minus actual, in addition to what it already shows.
- **Never put labels inside thin segments.** Put them outside or beside.

### 8.2 Interaction rules that bind every surface

- **Every accept / decline choice also offers Change,** in this order: primary · Change · negative. For example: "Approve · Change to… · Decline", or "Request 5 h · Change hours… · Not now". Change opens the item pre-filled, and submitting it counts as the decision. A plain Done or dismiss on an information-only item doesn't need it.
- **One verdict rule** (`lib/er.ts`). Never compute on-track / watch / at-risk locally. A why is owed only past ±4 h **and** ±$1k.
- **Capacity** = the person's nominal week minus time away. Target and surge are ticks, not colors. Execs are left out of studio capacity. The studio's Model and Surge figures are a SpannerOS studio setting.
- **The chrome teaches.** Labels explain themselves where the user meets them (for example, "↔ = on target (within ±4 h or ±$1k)").
- **Motion means a state change.** Nothing moves at rest; transitions are 0.15–0.3 s.
- **Voice:** labels and headings are lowercase, except the small-caps label rows. Explanations are sentence case in `--mut`. Use American English.

### 8.3 Tables, sorting and lists

- **Sortable headers show a cue:** a faint arrow at rest, the active one heavier with its rank. One multi-level sort everywhere ("sorted by A then B", with reset), remembered per browser (R-70).
- **Default order** (R-71): programs by client, then project, never by ID. People A to Z. Contractors at the end. The arrow is visible on load. A screen that is a ranking may say so and order by its measure.
- **Table headers align with their data** (R-72).
- **In program lists** a click selects, a double-click opens, and command-click opens a new tab (R-73).
- **Display settings are remembered per screen,** except the week. Present mode and "viewing as" are never stored (R-74).
- **Heavy summary panels collapse and remember it.** Empty status panels collapse to one compact line (R-75).
- **Rows expand to detail and edit in place** (R-76).
- **A program tag** is a 22 px color block on its own at the left, an 8 px gap, then the short name, with the TPL lined up under the name, all one size (R-78).
- **Another person's record opens read-only** with an explicit "edit on their behalf" (R-79).
- **Use a segmented row instead of a dropdown** for a short list (R-80).

**Member and contractor surfaces** add the rules in `reference/member-surface-ui-rules.md`. The ones most often broken:

- A control names its action, not its state.
- Emphasis marks the field being entered, never the derived one.
- Plan behind and wider, actual narrow and on top, on one shared scale.
- No field under 16 px, and every touch target at least 44 × 44.
- Density is a count problem, not a size problem: relocate, don't delete.
- A dead handler must not look like a dead control.

---

## 9 · The two skins

Torque is for product screens. The **brand skin** is for anything a client sees. The brand skin is **token overrides on the same names and the same markup** (`data-skin="brand"`), not a second system.

| | Torque | brand skin |
|---|---|---|
| surface | paper with glows · navy in dark | white; light only |
| header | navy bar, "spanner os" lockup | navy band, s07 wordmark lockup |
| panels | 16 px, glass / soft shadow | 6 px, `#D4D8DB` hairline, flat |
| labels | 12.5 px caps, tracked | 14.67 px bold, sentence case |
| headings, big numbers | 800 | 400, brand scale |
| primary button, active segment | azure, glow | navy, flat |
| chips · avatars · cells | pill · rounded square · 8 px | 4 px · circle · 3 px |
| confirmed | green | azure (the brand has no green) |
| estimate | estimate gray | estimate gray internally; navy dashed on the client report |
| project colors | the data palette | one client per report: azure / orange / navy |

Both skins share the layout, spacing, type below headings, tabular numerals, series meanings, money gating, field states and every interaction.

---

## 10 · Building

**Mockups (Cowork):**

1. Start from the shell in `mockups/spanneros-design-system.html` (built from `design/mockup-src/ds/` parts). Don't invent a new shell.
2. Put the mockup control strip (screen, viewing as, mode, skin, theme) **above** the sticky header, so it doesn't inflate the measured bar. It is not app chrome.
3. The footer states what the page is, its theme behavior, its money gate and its **functional reference**.
4. Test with Playwright at 2560, 1728 and 390 px × dark and light × torque and brand × edit and present. Route-abort Google Fonts. Fail on page errors or `scrollWidth > innerWidth`.
5. Run `/spanner-design-loop` for the review before delivery.

**App (Claude Code):**

- Use the existing `torque.css` classes and `app/(os)/_components`.
- Scope new CSS under `html[data-os]`.
- Read money only through the `lib/money*.ts` accessors.
- A new component joins `/admin/design-system` (A8) in the PR that builds it.
- Don't hand-edit a token in `torque.css` without changing the spec and the mockup source in the same change.

---

## 11 · Phone

The phone is a **second surface on the same routes**, not a responsive squeeze. Its unit is the day; the browser's is the week. The phone spec is the source; this is the floor.

**Choosing the surface:**

- The surface is chosen by a remembered `?view=phone|browser`.
- Every phone screen's `⋯` sheet offers "use the browser layout here", and that option is never gated.

**Content rules:**

- **One task, one hand.** Each screen answers one question and shows ≤12 numbers before scrolling.
- **Nothing is removed, only relocated.** Moved items go to a row tap, `⋯`, another tab, or an "open on desktop" card.

**Floors:**

- 44 × 44 targets
- inputs ≥16 px (`font-size:max(16px,1em)`)
- labels ≥12 px, chart axes ≥11 px
- `100svh`, never `100dvh`
- `env(safe-area-inset-*)`
- fields commit as you type
- input sheets put their actions in the header

**Shell:**

- A navy app bar: 20 px SpannerSans title and a sub line. There is no wordmark.
- Up to five bottom tabs per role, with inbox for everyone and "more" last, in lifecycle order.
- The comment rail becomes a sheet.
- Toasts offer undo for anything a thumb can do by accident.

**Components:**

- **Tables** become row cards unless the columns are one variable read across, such as a timesheet or ≤6 weeks.
- **Charts** show ≤6 weeks, tap for the crosshair, and nothing is hover-only.

**Modes and money:**

- Present on a phone means **follow-along**: read-only at the same type size (`--s` stays at 1).
- Money gating is identical to desktop, with no phone exception.

---

## 12 · Checklist before presenting any SpannerOS screen

- [ ] One layout; edit and present differ in chrome and read-only state, not just `--s`; the mode is in the URL
- [ ] Default theme follows the system, with a dark · light · system choice; light and dark both checked; native controls get a `color-scheme`; both skins where a client can see it
- [ ] Navy header with the "spanner os" lockup on a shared baseline, section prefix visible below 1440 px; top bar one row at ≥1100 px; account controls in the dock; sticky offsets measured
- [ ] Controls next to what they change, and in the same spot on every screen; program head steady
- [ ] Six sections in lifecycle order; the nav shows only screens the role can open
- [ ] Whole window used, with space where possible; tables size to content; comment rail present, scoped and adjustable
- [ ] Estimate and forecast series are gray (`--est`), never amber; over plan is a plain solid run past the plan, no hatch, no orange slice; estimate behind actual (R-116)
- [ ] Selected and reviewed weeks marked with labeled bands at the same x; one week anchor per screen
- [ ] Sortable headers show an arrow; default order is client then project, never ID
- [ ] Money: role × audience; $ disabled with a reason; "restricted", never blank or $0; Slack follows the channel
- [ ] Field states: entered / required / restricted; 0 is 0; "—" only for not set
- [ ] Short names, IDs in tooltips, "TPL", "Tin"
- [ ] Color = meaning audit; project colors from the palette; Tin labeled; gray only for internal and time away
- [ ] SVG colors via variables; actual stops at the last approved week; crosshairs synced
- [ ] Accept / decline choices offer Change
- [ ] Verdicts from the shared rule, not computed locally
- [ ] Tested at 2560, 1728 and 390 px with no page errors and no horizontal scroll
- [ ] Footer names the functional reference (mockups)
- [ ] American English throughout
- [ ] R-94 to R-128 checked (§13): neutral selected state, links, status pills not row tints, controls stay put, hover popovers, shared scales, save keeps your place

---

## 13 · Rules added since rev 1 (R-94 to R-128)

Full text and reasoning: `specs/spanneros-design-system.md` §11 and §12, Torque §12. R-94 to R-116 approved 2026-11-03 (interface-98 review, built on PRs #392–#396); R-117 to R-128 approved 2026-11-04 (walk-through mockup `mockups/261104-walkthrough-feedback.html`, not built yet).

| # | Rule |
|---|---|
| R-94 | A numbered section has a large badge (about 40 px) and a 24 px lowercase title; the lead section's badge takes its verdict color. |
| R-95 | Typed text is the most important thing on a review page: larger and bolder than its chrome, placed before the data it explains. |
| R-96 | One short line never gets a tall card; empty "required" strips stay one line. |
| R-97 | Blocks in a row share one height; stretch the panel, not its rows. |
| R-98 | Keep the reading order of the five sections as Giles set it. |
| R-99 | One click opens everything that needs attention; a click anywhere on a row opens it. |
| R-100 | One week label, "week of X", meaning the week the page is about. |
| R-101 | The page head is one sticky block down to the TPL line, on every program tab. |
| R-102 | Estimates draw gray, never yellow or amber. |
| R-103 | Program lists show the program color as a bar and the verdict as a pill (on track, watch, at risk), no row tint; short names; worst first or A–Z. |
| R-104 | A page with more than one reading gets a visible view switch; name views for what they show. |
| R-105 | A view that replaces an old one starts with both, and a gap note is written first. |
| R-106 | Don't pin a limit that isn't decided yet. |
| R-107 | Test at the width people see (wide, comment rail open); stack below about 520 px a column. |
| R-108 | Selected is neutral: light fill, 2 px ink ring, bold text; never an azure fill. Brand skin keeps solid navy. |
| R-109 | Azure marks actual data, the focus ring and the single primary action (#06A6ED). |
| R-110 | Links are blue and underlined: #0A7DB8 (#5CC6F7 dark), never the bright azure, never in fine print. |
| R-111 | Units live in the header; cells hold the number. |
| R-112 | An editable cell looks editable before you click it: outlined box, inset shadow, a hint when empty. |
| R-113 | A program page names its program at the top in a short-name headline; a program list never outranks it. |
| R-114 | Quiet states: in a signal table only watch and at risk get tinted pills; a program list shows a status pill on every row, no row tint. |
| R-115 | Controls stay put: a control that appears only sometimes gets reserved space. |
| R-116 | Estimate and actual are a pair: wider lighter estimate behind narrower solid actual, same program color; future weeks estimate only; no hatching. |
| R-117 | Every mark on a chart or diagram hovers to a popover with its detail and clicks to open its panel; one font; a scrollbar never covers a legend. |
| R-118 | Every phase row carries its phase icon (schedules, key dates, phase maps). |
| R-119 | Compared rows share one scale, keyed in the column header; a total row gets its own neutral scale. |
| R-120 | Focus without losing context: clicking an item in a diagram shrinks the diagram beside its detail, item lit, rest faded; close restores. |
| R-121 | A block's progress is a segmented bar (one segment per checklist item, green when checked, "n/m" or "✓ done"), like Forge's checkpoint bar; a completed block turns green. |
| R-122 | Checking an item records who and when, with an optional evidence link; a block-level "complete" records who and when and can be reopened. |
| R-123 | Claude's proposals appear in place, dashed azure, with their source and accept / skip; nothing is written until accepted. |
| R-124 | Today keeps the light-blue wash; the selected day or column gets a 2 px azure outline; a view of a day other than today carries an amber "Not today" note with "back to today". |
| R-125 | Saving keeps your place: no save scrolls the page back to the top. |
| R-126 | Typed totals are the record of time; timers and the calendar are a reference beside each total (agrees / differs, "=" takes it, rounded up to the quarter hour) and never change a total on their own. |
| R-127 | Anything outside the agreement gets no dates and is drawn faint or folded into one row. |
| R-128 | An editor or detail replaces the side panel in place, with "← back", instead of a drawer over the page. |

**Also settled:** "five bands" keeps its name; right-click on a program opens W4 and long-press does the same on touch; my week reaches any week the forecast covers.

---

## 14 · Pending, not yet rules

Mason put these on hold on 2026-10-23. Don't build to them as rules, and don't contradict them.

- **Type-size floors (R-61):** chart text stays large and labels are never clipped. He wants comparison examples before a floor is set.
- **Amber contrast and options (R-62):** a contrast rule for amber text and fills against navy and in light, or a different amber. He wants examples.
- **Estimate gray treatment:** the gray must look different from the reserved gray family. The exact treatment is not settled.
- **Explicit close on every inline panel (R-13)**, **pare Claude-produced pages to an exec summary first (R-35)**, **section headers larger than the biggest text in their box (R-48)**, **no bolder-than-bold type (R-91)**, **client output uses the brand skin as a fixed rule (R-93; he wants options for a client skin vs the SpannerOS style, to be decided by the team later):** none decided yet.
