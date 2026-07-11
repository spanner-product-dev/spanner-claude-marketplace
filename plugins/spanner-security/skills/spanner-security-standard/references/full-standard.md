# Spanner PD — App Security Standard (full reference)

The complete, secure-by-default standard. The SKILL.md summary points here for anything it doesn't fully answer. Read this before setting up a new repo or database, or before adding tables that hold financial, health, or government-ID data.

## Table of contents
- The three-layer compliance framework
- 1. GitHub rules — required in every repo
- 2. Supabase rules — required in every project
- 3. Cloudflare rules — the perimeter in front of every deployed app
- 4. New-project checklist
- Quick reference — the five rules that matter most

---

## The three-layer compliance framework

| Layer | Triggers | What it requires |
|---|---|---|
| **Layer 1 — Privacy (always on)** | Any users, any data | GDPR (EU users), CCPA (California — applies to us now), privacy policy, cookie consent, breach-notification process (72 hr for GDPR), data-deletion capability |
| **Layer 2 — Enterprise trust (always on)** | B2B / enterprise customers | SOC 2 Type II. Begin 9–12 months **before** the first enterprise deal, not after they ask. Controls must be real and evidenced, not just documented. |
| **Layer 3 — Regulated data (add as soon as practical)** | Payments, financial data, health data | PCI DSS (use Stripe to keep card data out of our scope), HIPAA (health data + BAA), financial-data rules. Add proactively when consequences are severe. |

Two operating principles: Layers 1 and 2 are always on (they shape architecture from day one, never bolted on later); and regulate to consequences, not just legal triggers (if the customer impact of a breach would be severe, build to the higher layer even when no law requires it yet).

---

## 1. GitHub rules — required in every repo

**Org context:** All code lives in the `spanner-product-dev` GitHub org (github.com/spanner-product-dev), Mason is Owner.

**Org-level (set once, enforced for all repos):**
- Secret scanning enabled (Global Advanced Security) — done 2026-05-28
- Push protection enabled — block commits that contain detectable secrets before they land
- 2FA required org-wide — done 2026-05-28
- Dependabot alerts + security updates enabled
- Base permission for members: **Read** (grant write per-repo, least privilege)

**Per-repo (required before a repo is considered compliant):**
- `main` is a protected branch: no direct pushes, PR required, at least 1 review
- No secrets in code — ever. Use environment variables / platform secret stores
- `.env`, `.env.*`, key files, and `*.pem` are in `.gitignore` from the first commit
- A `.env.example` documents required variables with **placeholder** values only
- README states which Layer(s) apply and links this standard

**If a secret is ever exposed:** deleting the file is not enough — git history still contains it. **Revoke and rotate** the key in the issuing platform (Supabase, Cloudflare, Stripe, etc.) first, then remove it from code and history.

---

## 2. Supabase rules — required in every project

Supabase is the database and auth for all projects.

**Authentication**
- Use **Supabase Auth** — never hand-roll authentication
- MFA enabled; prefer passkeys/authenticator app over SMS (SMS is SIM-swappable)
- Passwords are hashed by the provider (Argon2id-class) — never stored or logged in plaintext

**Authorization & Row-Level Security (the core rule)**
- **RLS enabled on every table that holds tenant or user data — from the first migration.** This is non-negotiable. RLS pushes the tenant filter into the database, so a bug in app code can't leak data across tenants.
- Default to **deny by default**, then write explicit allow policies. (ServiceNow leaked 1,000+ instances in 2024 by defaulting to "any user.")
- Authorize **server-side, always.** Hiding a UI button does not protect the API.
- Before returning any record, verify the user owns or may access it (prevents BOLA — the #1 app-security bug).
- **Never join an RLS table to a non-RLS table** — it can leak data transitively. Every joined table needs its own policy.

**Keys**
- The `service_role` key bypasses RLS — it lives **only** in server-side environments, never in client code, never in the browser bundle, never in the repo.
- The `anon` key is the only key allowed client-side, and it relies on RLS for protection.
- Rotate keys on any suspected exposure.

**Encryption**
- In transit: TLS/HTTPS everywhere (default)
- At rest: AES-256 (Supabase handles automatically)
- Field-level: encrypt SSNs, financial account numbers, and government IDs at the application layer (Layer 3)

---

## 3. Cloudflare rules — the perimeter in front of every deployed app

Cloudflare is the network perimeter for all deployed apps (e.g., the internal portal on Cloudflare Pages).

- HTTPS enforced; "Always Use HTTPS" on; HSTS enabled
- TLS minimum version 1.2 (1.3 preferred)
- WAF (Web Application Firewall) enabled on public-facing apps
- Rate limiting on auth endpoints and APIs — blunts credential-stuffing
- Bot Fight Mode / bot management on public apps
- DDoS protection on (default)
- Access control for internal-only tools: Cloudflare Access in front of anything not meant for the public, gated to `@spannerpd.com` — defense in depth beyond Google SSO
- Secrets for Workers/Pages live in Cloudflare environment variables / secret store, never in the repo

---

## 4. New-project checklist — run when starting anything

Run top to bottom before writing feature code. Claude follows this automatically; humans use it to verify.

**Repo setup**
- [ ] Repo created in `spanner-product-dev` org (inherits secret scanning, push protection, 2FA)
- [ ] `main` protected; PR + review required
- [ ] `.gitignore` includes `.env`, `.env.*`, `*.pem`, key files — committed first
- [ ] `.env.example` with placeholder values only
- [ ] README names applicable Layer(s) and links this standard

**Supabase setup**
- [ ] Supabase Auth wired (no custom auth)
- [ ] **RLS enabled on every data table in the first migration; deny-by-default policies written**
- [ ] `service_role` key server-side only; `anon` key the only client key
- [ ] Server-side authorization checks on every data-returning endpoint
- [ ] Field-level encryption planned for any SSN / financial / gov-ID data

**Cloudflare / deploy**
- [ ] HTTPS enforced, HSTS on, TLS ≥ 1.2
- [ ] WAF + rate limiting on auth/API endpoints
- [ ] Cloudflare Access gate for internal-only tools (`@spannerpd.com`)
- [ ] Deploy secrets in platform secret store, not the repo

**Compliance layer**
- [ ] Layer 1 confirmed on: privacy policy, cookie consent, data-deletion path, breach-notification process
- [ ] Layer 2 considered if enterprise customers are on the horizon (start SOC 2 9–12 mo ahead)
- [ ] Layer 3 added if the app touches payments, financial, or health data — or if breach consequences are severe

---

## Quick reference — the five rules that matter most

1. **No secrets in repos** — env vars only; revoke + rotate if exposed.
2. **RLS on every data table, from the first migration, deny-by-default.**
3. **Authorize server-side** — verify ownership before returning any record.
4. **`service_role` key never leaves the server.**
5. **Layers 1 & 2 always on; Layer 3 when consequences are severe.**

---

_Derived from `SpannerOS/Security Framework/spanner-security-standard.md` (the studio's canonical standard). If that document and this reference ever disagree, the canonical document wins — update this skill to match._
