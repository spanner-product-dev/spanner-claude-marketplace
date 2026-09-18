---
name: spanner-brand-voice
description: >
  Applies Spanner's brand voice and guidelines to any content creation or review task.
  Use this skill whenever writing or editing content for Spanner, Inc. — cold outreach
  emails, LinkedIn posts, newsletters, slide copy, proposals, follow-up emails, case
  study text, or any client-facing material. Also triggers on: "make this on-brand,"
  "Spanner voice," "write for Spanner," "does this sound like us," "rewrite in our
  tone," "draft a pitch email," "write a LinkedIn post," or any content request made
  in the Spanner Brand workspace. When in doubt, use this skill — catching an off-brand
  draft is much better than producing one without it.
---

# Spanner Brand Voice

You're creating or reviewing content for Spanner, Inc. — a premier Silicon Valley product
development studio. Spanner has a well-defined brand voice: expert but approachable,
transparently honest, collaborative, and always oriented toward the client's goals. Your job
is to produce content that sounds unmistakably like Spanner.

## Step 1: Load the Guidelines

Read both files from the user's workspace folder:

- **`brand-voice-guidelines.md`** — the full brand voice spec: voice attributes, messaging
  framework, tone-by-context matrix, terminology guide, and content examples
- **`content-guide.md`** — channel-specific quick reference: cold email structure, LinkedIn
  post format, newsletter patterns, slide copy rules, and the type accent system

These files live in the Spanner Brand project folder. If you can't find them, let the user know
and suggest running `/brand-voice:generate-guidelines` to rebuild them.

## Step 2: Read the Request

Before writing anything, identify:

- **Content type** — cold email, LinkedIn post, newsletter, slide copy, proposal, follow-up, etc.
- **Audience / persona** — which client type does this target?
  - *Startup Sam*: founder, VC-backed, first-time hardware builder — values trust and speed
  - *Growing Gabe*: Series B VP, experienced — wants a peer, not a vendor
  - *Tech Enterprise Ted*: large company director — values augmentation and reliability
  - *New Product Nic*: non-tech enterprise — needs guidance and realistic expectations
  - *Partner Patty*: agency/studio partner — values trust and gap-filling
- **Tone target** — use the tone-by-context matrix from the guidelines to dial in the right
  formality, energy level, and technical depth for this channel
- **Goal** — what outcome does this content need to drive?

## Step 3: Apply Voice Constants

These rules apply to every piece of Spanner content without exception:

| Rule | Do | Don't |
|------|----|-------|
| Pronoun | "we" | "I" (implies freelancer, not studio) |
| Company name | Spanner | "Spanner PD," "spanner" (lowercase in body) |
| Emphasis | Sentence structure, Azure text, or bold | ALL CAPS (except acronyms) |
| Opener | Lead with client's world | "Hope this finds you well," "Just checking in" |
| Closer / CTA | One specific, low-friction ask | "Let me know if you have questions" |
| Descriptor | "product development studio" | "firm," "agency," "vendor" |
| Tagline | what's next. (no quotes; period standalone) | "what's next" (in quotes) |

## Step 4: Write for the Channel

Use the channel-specific structure from content-guide.md. Key patterns:

**Cold email** — Hook (their world) → Relevance (their challenge) → Proof (one signal) → CTA (one ask). Never start with "I" or a service list.

**LinkedIn post** — Hook (counterintuitive observation, problem, or short story) → Point of view or insight → Close (question or clear takeaway). No "Excited to announce."

**Newsletter** — Open with a problem the reader recognizes → One specific, actionable idea → Clear takeaway. Give something useful; don't publish for its own sake.

**Slide copy** — Lowercase headers; sentence case body; one accent method per surface (Azure text, bold, or highlight — never combined); stats over descriptions ("400+ years cumulative expertise" beats "we're experienced").

**Proposal** — Mirror client goals first, then describe Spanner's approach. Phase-by-phase structure. End with "together."

## Step 5: Validate Before Presenting

Run through this checklist mentally before showing the output:

- [ ] "we" not "I" throughout
- [ ] No filler openers or zero-value closers
- [ ] Opens with client's world (outreach) or their stated goals (proposals)
- [ ] Single CTA for outreach; clear next step for proposals
- [ ] No ALL CAPS emphasis
- [ ] "Spanner" cased and used correctly
- [ ] Technical depth matches the channel and persona
- [ ] Tagline formatted correctly if used

## Step 6: Logo References in Content

Some content surfaces (email signatures, proposal cover pages, slide masters,
press kits, newsletter mastheads) need to *reference* or *embed* the Spanner logo.
When that comes up, point to the right file. Logo files are bundled in the
`spanner-brand-visual` skill at `assets/Logo/` (or via the public URL mirror at
`https://raw.githubusercontent.com/spanner-product-dev/spannerpd-brand-assets/main/brand/Logo/`).
The selection rules below name files relative to that root:

- **External-facing materials** → always pull from
  `Logo/0_Spanner Logo Package (External Sharing OK)/` — that folder is the approved set
- **Email signature** → `0_Spanner Logo Package (External Sharing OK)/2024_Azure_Refresh/Spanner_Logo_Azure_2024_320px.png`
  on light backgrounds (current 2024 Azure)
- **Proposal / case study cover** → `2024_Azure_Refresh/Spanner_Logo_Azure_2024_640px.png`
  on white, or `Spanner-Logo-White-Rev-01.png` on a Navy block
- **Slide deck (web/digital export)** → `2024_Azure_Refresh/Spanner_Logo_Azure_2024_640px.png`
  or `_1280px.png` for hero slides
- **Press kit / partner request** → share the whole `0_Spanner Logo Package` folder
  (recipient gets the 2024 Azure refresh subfolder + the legacy Blue/White/Dark Gray/
  square/rectangle set)
- **Print collateral** → SVG (current Azure, scales) or legacy Blue EPS
  (`Spanner_Logo_Blue.eps` / `150810_Spanner_Logo_White-only.eps`) until a 2024-Azure EPS
  is re-exported by a designer
- **QR code center mark** → `2_Export Logo Files/Logos for QR Codes/`
- **Source files for a designer** → `1_Native Logo Files/` (.ai source)

Two things to flag if relevant to the content you're writing:

1. **Never reference `z_Archive/`** — those are old WIP revisions
2. **Legacy-blue caveat** — the original Blue PNG/SVG/EPS files use the older 2015
   Spanner Blue `#49B5CF`, not current Azure `#06A6ED`. The `2024_Azure_Refresh/`
   subfolder fixes this for SVG and PNG. Default to the refresh; only reach for the
   legacy Blue EPS when you need EPS for print and a 2024-Azure EPS hasn't been
   re-exported yet.

For full file inventory and selection logic, the `spanner-brand-visual` skill carries
the complete table.

## Step 7: Present with Brand Notes

Show the content, then add a short **Brand choices** section explaining 2–3 key decisions: why this opening, what tone register was chosen, how the CTA was framed. This helps the user understand the reasoning and gives them a clear handle for giving feedback.

If any part of the guidelines is flagged as Medium confidence (e.g., tone matrix not yet validated against call transcripts), note it briefly — the user should know the basis for those choices.

End by offering to: refine the current draft, try a different persona, or write a follow-up version.
