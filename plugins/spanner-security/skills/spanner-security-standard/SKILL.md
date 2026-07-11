---
name: spanner-security-standard
description: >
  Spanner PD's secure-by-default engineering standard — GitHub, Supabase, and Cloudflare rules plus the three-layer compliance framework (privacy, enterprise trust, regulated data). Apply this skill automatically, without being asked, whenever building or reviewing anything touching code, data, auth, or deployment: starting a repo or project, writing a Supabase migration or query, adding authentication, writing an API route or server action, setting up RLS, handling secrets or env vars, configuring Cloudflare, or adding a table/column holding user, tenant, financial, health, or personal data. Also triggers on "is this secure", "security review", "new project setup", "add RLS", "secure by default", "handle secrets", or any request in the spanner-product-dev GitHub org, SpannerOS, or a Spanner client project. When in doubt, apply it — retrofitting security is far more expensive than baking it in, and one leaked key or missing RLS policy can expose every tenant.
---

# Spanner PD — Security Standard

This is the source-of-truth security standard for everything Spanner Product Development builds. It is **secure by default, not retrofitted** — it shapes architecture from day one and is never bolted on later. Follow it automatically when building any project; treat it as the bar every repo, database, and deployed app must clear.

## Two operating principles (established by Mason)

1. **Layers 1 and 2 are always on.** They shape architecture from day one — never bolted on later.
2. **Regulate to consequences, not just legal triggers.** If the customer impact of a breach would be severe, build to the higher layer even when no law requires it yet.

## The five rules that matter most

Get these right and most breaches never happen. The rest of the standard supports them.

1. **No secrets in repos** — environment variables / platform secret stores only. If a secret is ever exposed, deleting the file is not enough (git history keeps it): **revoke and rotate** the key in the issuing platform first, then remove it.
2. **RLS on every data table, from the first migration, deny-by-default.** Row-Level Security pushes the tenant filter into the database, so a bug in app code can't leak data across tenants. Default to deny, then write explicit allow policies.
3. **Authorize server-side** — verify the user owns or may access a record *before* returning it. Hiding a UI button does not protect the API. This prevents BOLA, the #1 app-security bug.
4. **The `service_role` key never leaves the server.** It bypasses RLS. It lives only in server-side environments — never in client code, the browser bundle, or the repo. The `anon` key is the only client-side key.
5. **Layers 1 & 2 always on; Layer 3 when consequences are severe.**

## How to apply this skill

When you're **building**, run the New-Project Checklist (below) before writing feature code, and hold every migration, API route, and deploy config to the five rules above. When you're **reviewing**, read the code against the checklist and the full standard and flag anything that deviates — an unguarded table, a `service_role` key that could reach the client, a secret in the repo, a missing privacy-layer control.

For anything beyond the summary here — the exact GitHub org settings, the full Supabase authorization rules, the Cloudflare perimeter config, or the three-layer compliance framework and when each layer applies — read `references/full-standard.md`. Read it whenever a decision isn't fully answered by the five rules, and always before setting up a brand-new repo or database or before adding tables that hold financial, health, or government-ID data.

## New-Project Checklist — run before feature code

Run top to bottom before writing feature code. You follow this automatically; humans use it to verify.

**Repo setup**
- [ ] Repo created in the `spanner-product-dev` org (inherits secret scanning, push protection, 2FA)
- [ ] `main` protected; PR + at least 1 review required; no direct pushes
- [ ] `.gitignore` includes `.env`, `.env.*`, `*.pem`, and key files — committed first
- [ ] `.env.example` with **placeholder** values only
- [ ] README names the applicable Layer(s) and links this standard

**Supabase setup**
- [ ] Supabase Auth wired (never hand-roll authentication); MFA on, passkeys/authenticator over SMS
- [ ] **RLS enabled on every data table in the first migration; deny-by-default policies written**
- [ ] `service_role` key server-side only; `anon` key the only client key
- [ ] Server-side authorization on every data-returning endpoint (verify ownership before returning)
- [ ] Never join an RLS table to a non-RLS table
- [ ] Field-level encryption planned for any SSN / financial-account / government-ID data

**Cloudflare / deploy**
- [ ] HTTPS enforced, HSTS on, TLS ≥ 1.2
- [ ] WAF + rate limiting on auth/API endpoints
- [ ] Cloudflare Access gate for internal-only tools (`@spannerpd.com`)
- [ ] Deploy secrets in the platform secret store, not the repo

**Compliance layer**
- [ ] Layer 1 confirmed on: privacy policy, cookie consent, data-deletion path, breach-notification process
- [ ] Layer 2 considered if enterprise customers are on the horizon (start SOC 2 9–12 months ahead)
- [ ] Layer 3 added if the app touches payments, financial, or health data — or if breach consequences are severe

## When to escalate a layer

- **Layer 1 (Privacy) — always on.** Any users, any data. GDPR/CCPA, privacy policy, cookie consent, 72-hour breach notification, data deletion.
- **Layer 2 (Enterprise trust) — always on for B2B.** SOC 2 Type II; begin 9–12 months *before* the first enterprise deal, not after they ask.
- **Layer 3 (Regulated data) — add as soon as practical.** Payments (use Stripe to keep card data out of scope), health data (HIPAA + BAA), financial-data rules. Add proactively when the consequences of a breach would be severe, even if no law requires it yet.

See `references/full-standard.md` for the full framework, the per-platform rules, and the reasoning behind each control.
