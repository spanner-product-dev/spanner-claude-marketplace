---
name: spanneros-design-system
description: Rules for designing, building or reviewing any SpannerOS screen, mockup or component: layout, edit/present modes, shell, money gating, field states, palette, components, charts, skins, phone.
---

# SpannerOS design system

This skill covers how SpannerOS screens are put together: one layout with edit and present modes, the shell, money gating, field states, names, color, components, charts, the brand skin and the phone surface. It sits on top of **Torque**, the visual language (tokens, glass panels, type). Use it for any SpannerOS work, including the app (`spanner-planner`), HTML mockups, portal tools that live inside SpannerOS, and Arne's Forge (BD) build.

**Don't use it for** client-facing collateral, decks, documents, proposals or marketing pages. Those follow `spanner-brand-visual` and `spanner-brand-voice`. The one exception is a SpannerOS screen a client signs in to see, which uses this system's **brand skin** (§9).

_Snapshot of the rules as of 2026-10-07 (design system rev 1, IA rev 1, phone rev 1, plus later decisions)._

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
- **When sources disagree, the newer dated decision wins.** The specs were brought up to date on 2026-10-07.
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
/* Torque — dark (the default) */
html[data-theme="dark"]{
  --bg:#293A49; --bgglow1:rgba(6,166,237,.10); --bgglow2:rgba(226,103,42,.05);
  --panel:rgba(255,255,255,.045); --panel2:rgba(255,255,255,.075); --line:rgba(255,255,255,.10);
  --tx:#E8EEF4; --mut:#93A3B2; --dim:#5E6E7D;
  --azure:#1FB2F5; --orange:#ED7A40; --amber:#D9A514; --green:#2EC592; --lblue:#CAECF6;
  --shadow:none; --glow:0 0 36px rgba(6,166,237,.07); --inbg:rgba(0,0,0,.25); --stick:#314254;
  --e2:0 0 0 1px rgba(255,255,255,.08),0 18px 48px rgba(0,0,0,.35);
  --hdr-bg:#1D2B37;
}
/* Torque — light */
html[data-theme="light"]{
  --bg:#F4F7F9; --bgglow1:rgba(6,166,237,.06); --bgglow2:rgba(226,103,42,.03);
  --panel:#FFFFFF; --panel2:#FFFFFF; --line:#DCE3E8;
  --tx:#293A49; --mut:#6B7A8A; --dim:#97A2AC;
  --azure:#06A6ED; --orange:#E2672A; --amber:#B58A10; --green:#0B7C58; --lblue:#CAECF6;
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

- **Dark is the default everywhere** (Mason, 2026-10-07).
- Each person picks dark, light or "follow the system". That is a three-way select, not a toggle, remembered in local storage under `sos-os-theme`. The old key `sos-torque-theme` is read as a fallback.
- A pre-paint script sets the theme before the first frame.
- Every surface is still checked in both themes.

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
- **Side nav breakpoints:** ≥1280 px expanded and collapsible (collapse is a per-person local-storage convenience); 900–1279 px icons only, opens on tap; <900 px off-canvas behind ☰.

### 4.2 Top bar

- **The bar is navy with white text in every skin and both themes.** It is `#293A49`, or `#1D2B37` in dark so it still reads as a bar. It is 66 px tall.
- **Controls on the bar** use the `--hdr-*` tokens. A selected segment is light azure with navy text, because white on azure fails 4.5:1.
- It holds only what changes the whole screen:
  - lockup and crumb
  - audience indicator
  - week stepper
  - $ ⇄ h
  - "viewing as" (admin only)
  - theme
- It fits on one row at ≥1100 px. Chart and row controls sit on the chart or row (DR-6).
- **Header lockup** (Mason, 2026-10-06; exact CSS in Torque §5):
  - The wordmark is **"spanner os"**: lowercase, with a space, and "os" in azure. It is SpannerSans at **42.4 px**, which gives the brand's 30 px of ink and 22.2 px letters. "spanner" itself never changes.
  - The **crumb** after the divider is Inter 22 px regular, letter-spacing .04em.
  - **Dividers** are 28 px, 1 px azure *borders* centered on the letter body. Never draw them as 1 px backgrounds, and never align them on an empty flex item's synthesized baseline.
  - Everything sits on one shared text baseline. Below 620 px the lockup scales to 0.7.
  - Don't put a logo SVG on Torque pages.
- **"Viewing as"** previews another role's *layout* with the admin's own data and permissions. It lives in a cookie and is never in a URL.

### 4.3 Comment rail, width and sticky elements

- **The comment rail** sits on the right of every meeting screen (DR-3): a summary block, the scope chips (week · program), threads, and the composer in edit. It is 320 px docked (360 at ≥2200) and becomes a drawer below 1280.
- **There is no max-width on meeting screens** (DR-2).
  - Panels flow into auto-fit columns: min 520 px, wide panels 700 px.
  - Tables size to their content. Spare width goes to weeks, charts or the rail.
  - Side padding is 24 px (16 on a phone).
  - Documents and portal articles keep a max-width.
- **Measure sticky offsets** from the bar with a ResizeObserver. Never hardcode them. Measure chart geometry the same way.
- **Every section route has a loading skeleton.**

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
- Write **"TPL"**, never "lead". Apple programs are always **"Tin"**.

### 5.3 Field states

A human field has three states, never two, and "restricted" is not "empty":

- **entered**
- **required — not entered**: an orange dashed strip, counted in a header meter
- **restricted**: a neutral hatched chip saying content exists

Never render a bare blank. Elsewhere:

- **0 renders as 0.** "—" means only "not set".
- **"no actuals"** is for a *suspected data gap* only. A real zero is an ordinary under-gap with a why.

---

## 6 · Color

**Color is information, never decoration.** If a color doesn't carry one of these meanings, it doesn't appear.

| Meaning | Color |
|---|---|
| actual · interactive | azure |
| warning · over | orange |
| estimate | amber |
| confirmed · on target | green (azure on the brand skin) |
| time away · NB · internal | gray family |
| alerts only | red (almost never on a page; **red is never a status**) |

**Status words:** **on track** green · **watch** amber · **at risk** orange.

**Series:**

- **Actual:** azure, heaviest stroke. It stops at the last approved week with a dot.
- **Estimate:** amber. The tolerance band is amber at 14% (±4 h / ±$1k).
- **Baseline and Model:** ink, dashed, at 55%.
- **Budget and Surge:** orange, dashed.
- **This or the reviewed week:** an azure 8% band.

**Utilization** is three buckets, never collapsed:

- hourly billable: azure
- milestone in-scope: azure hatched
- NB: gray `#97A2AC`

**Time away** is hatched silver in every bar, so it can't read as a gray program.

**Project identity** (`lib/palette.ts`, ratified Q-050):

- **Generic programs** take these hues in this order, assigned by sorted position among the *active* generics, so colors re-balance as work turns over: orange `#E2672A` · plum `#8D4A86` · olive `#6F7D2F` · rose `#C77E8E` · green `#1E7D4F` · violet `#6A5FA8` · sienna `#9C4A14` · amber `#D9A514` · berry `#B23A6F`.
- **Tin owns the blues,** assigned by launch date and alternating light and dark: sky `#6FC6F2` · steel `#2E7FAD` · azure `#06A6ED` · deep `#04679C` · cornflower `#4F93C4`. Midnight is retired. **A Tin segment always carries its label.**
- **The gray family is reserved and never assigned to a client:** DTO/holiday `#B9C1C8` · NB `#97A2AC` · OOO contractor `#76828D` · leave `#55606B`.
- **Grid tone:** capacity-grid and allocation fills use the hue at 62% over the panel, with navy labels. Charts keep the solid hue.
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
| KPI tile | one number pair, unit muted, optional meter; warn | cost tile finance-only |
| Stacked bar by program | approved solid · forecast faded; Model/Surge lines | $ or h |
| Actual vs estimate | actual to last approved + dot; estimate; band; gap label | $ or h |
| Signed gap bar | over (orange) · under (dashed) · on target ↔ · no actuals | $ or h |
| Allocation bar | assigned · open · away (hatched) · over available (orange outline) · nothing assigned | none |
| Data-check card | problem · info · fixed; present shows the count | none |
| Approval gate | TPL TRUE → studio manager approves in Harvest → Mason's green light | none |
| Decision buttons | primary · **Change** · negative | Δ$ only when allowed |
| Slack draft | draft · posts after the green light; deep link | follows the channel |
| Chips | on track · watch · at risk · pending · TRUE · drifted · what-if · complete · source (edit only) · basis badge | — |

**Visual specs:**

- **Panels:** 16 px radius, 1 px `--line`, `--panel` fill.
- **Primary button:** azure with white 800 text and a glow. **Ghost button:** line border.
- **Chips:** pills with a 12% tint fill, a 35% tint border and colored text (`color-mix`).
- **Segmented controls:** the active segment is azure.
- **Tables:** hairline rows, right-aligned numerics, an opaque `--stick` first column when sticky.
- **Avatars:** rounded squares with azure-tint initials.
- **Inputs:** `--inbg` fill; focus is an azure border with no outline ring.

---

## 8 · Charts and interaction rules

### 8.1 Charts

- **Use hand-rolled inline SVG only** (no chart libraries). Every color is a CSS variable via `style="fill:var(--azure)"`. Project hexes and the gray family are the only literals. That way the theme toggle restyles charts with no re-render.
- **Axes and legends:** the x axis is Monday dates, thinned to every other label below 46 px per week. Put a one-line legend under the chart and the fuller key in a popover next to it.
- **Crosshairs sync across every chart on a page.** The tooltip shows in the hovered chart.
- **Never put labels inside thin segments.**

### 8.2 Interaction rules that bind every surface

- **Every accept / decline choice also offers Change,** in this order: primary · Change · negative. For example: "Approve · Change to… · Decline", or "Request 5 h · Change hours… · Not now". Change opens the item pre-filled, and submitting it counts as the decision. A plain Done or dismiss on an information-only item doesn't need it.
- **One verdict rule** (`lib/er.ts`). Never compute on-track / watch / at-risk locally. A why is owed only past ±4 h **and** ±$1k.
- **Capacity** = the person's nominal week minus time away. Target and surge are ticks, not colors. Execs are left out of studio capacity. The studio's Model and Surge figures are a SpannerOS studio setting.
- **The chrome teaches.** Labels explain themselves where the user meets them (for example, "↔ = on target (within ±4 h or ±$1k)").
- **Motion means a state change.** Nothing moves at rest; transitions are 0.15–0.3 s.
- **Voice:** labels and headings are lowercase, except the small-caps label rows. Explanations are sentence case in `--mut`. Use American English.

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
| estimate | amber | amber internally; navy dashed on the client report |
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
- [ ] Dark by default with a dark · light · system choice; both themes checked; both skins where a client can see it
- [ ] Navy header with the "spanner os" lockup on a shared baseline; top bar one row at ≥1100 px; sticky offsets measured
- [ ] Six sections in lifecycle order; the nav shows only screens the role can open
- [ ] No max-width on meeting screens; tables size to content; comment rail present and scoped
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
