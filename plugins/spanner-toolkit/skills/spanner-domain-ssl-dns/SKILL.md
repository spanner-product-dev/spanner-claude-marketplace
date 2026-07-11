---
name: spanner-domain-ssl-dns
description: Diagnoses and fixes SSL/DNS problems on Spanner's domains (spannerpd.com, spannerproductdevelopment.com, and any future Squarespace-connected, GoDaddy-managed domain). Use whenever Mason reports an SSL/certificate error, "Your connection is not private", a site that works with www but not without it (or vice versa), a domain "not working", DNS questions ("is our DNS right?", "check the A records"), redirect problems between apex and www, or anything touching GoDaddy DNS or Squarespace domain settings. Also use before/after any GoDaddy DNS change to verify state. When in doubt, use this skill — it encodes the sandbox's DNS-lookup workaround and two GoDaddy traps (forwarding overrides, re-parking) that cost hours to rediscover.
---

# Spanner Domain SSL/DNS Troubleshooting

Distilled from the Jul 8 2026 spannerpd.com apex SSL fix. The full beginner-level
runbook with click-by-click GoDaddy/Squarespace steps lives in Notion:
"Fix the spannerpd.com SSL Error" (child of the SEO & AEO Quick Wins playbook,
https://app.notion.com/p/397222a7d40981f19d8de076adda2d71). This skill is the
diagnostic brain; link the runbook when handing steps to a non-technical person.

## Spanner's setup (assume this unless told otherwise)

| Thing | Value |
|---|---|
| Website host | Squarespace (site: spannerpd.squarespace.com) |
| DNS host / registrar | GoDaddy — nameservers ns73/ns74.domaincontrol.com |
| Primary domain | spannerpd.com (www prefix ON → apex 301s to www) |
| Secondary domain | spannerproductdevelopment.com (also Squarespace-connected) |
| Correct apex A records (all four required) | 198.185.159.144 · 198.185.159.145 · 198.49.23.144 · 198.49.23.145 |
| Correct www record | CNAME → ext-cust.squarespace.com |
| Email | Google Workspace (don't touch MX); a `mail` A record exists — leave it alone |
| Squarespace SSL setting | Settings → Developer Tools → SSL → Secure (Preferred) + HSTS |

## Step 1 — Diagnose before advising

The Cowork sandbox has **no raw network**: `dig`, `curl`, and `openssl` all fail
("network unreachable"). Don't waste turns on them. Instead:

1. **DNS-over-HTTPS via web_fetch** (works in the sandbox):
   - `https://dns.google/resolve?name=<domain>&type=A` (also `type=NS`, `type=CNAME` for www)
   - Caveat: Google may serve a cached answer for up to the record's TTL (Spanner's
     records are 600s). The `Comment` field names the upstream server — 173.201.x/97.74.x
     means it came from GoDaddy's nameservers.
2. **Ground truth — ask Mason to run in Terminal** (bypasses every cache):
   ```
   dig @ns73.domaincontrol.com <domain> A +short
   ```
   Whatever this returns is what GoDaddy is actually publishing, regardless of
   what the GoDaddy zone editor *displays*.
3. To see the browser reality, ask for an **incognito** test (normal windows cache
   redirects and cert states) or a screenshot of the GoDaddy DNS table.

## Step 2 — Interpret the IPs

| dig/DoH returns | Meaning |
|---|---|
| All four 198.185.159.x + 198.49.23.x | Correct — Squarespace is serving the apex |
| Only two of the four | Records missing or a typo (check digit-by-digit — a `.245` for `.145` cost us an hour) |
| 15.197.x.x and/or 3.33.x.x | **GoDaddy forwarding/parking infrastructure** (AWS Global Accelerator). A Forwarding rule or Parked state is overriding the zone — the A records in the editor are NOT being served |
| `Parked` literal in the GoDaddy table | Domain is parked; delete that record |

## The two GoDaddy traps (why this skill exists)

1. **Forwarding rules silently override apex A records.** The DNS Records tab can
   show four perfect A records while the Forwarding tab (DNS → Forwarding) causes
   GoDaddy to publish its forwarder IPs instead — with no valid certificate for the
   apex. On a Squarespace-connected domain, registrar-level domain forwarding must
   be **OFF**; Squarespace's "Use www prefix" setting does the apex→www 301 itself,
   with a proper cert.
2. **Deleting a forwarding rule re-parks the domain.** GoDaddy wipes the `@` A
   records and substitutes a single `A @ Parked` record. Expect it; don't panic.
   Delete the Parked record and re-add the four Squarespace A records.

## Fix sequence (GoDaddy side)

1. DNS → **Forwarding** tab: delete any forwarding on the domain (Domain and Subdomains → "Not set up").
2. DNS → **DNS Records**: delete any `A @ Parked` record and any `@` A record not in the four.
3. Ensure exactly four `A @` records (the table above), TTL default. Keep the www
   CNAME, `mail` A record, NS rows, and MX untouched.
4. Squarespace: Settings → Developer Tools → SSL = **Secure (Preferred)** + HSTS.
   Nothing else to click — the cert extends automatically once DNS is right
   (usually 15–60 min). If still broken after 24h, Squarespace support chat:
   "apex missing from SSL certificate, DNS now has all four A records — please
   force a certificate reissue."
5. Do NOT enable DNSSEC during troubleshooting (a bad signing takes the whole
   domain down for hours). It's a separate, deliberate hardening task.

## Verification (done = all three)

1. `dig @ns73.domaincontrol.com <domain> A +short` → the four 198.x IPs.
2. Fresh incognito: `https://<apex>` → padlock, silent 301 to `https://www.<apex>`.
3. `https://www.<apex>` still loads normally.

## After fixing

- Log it: matrix task update (matrix-task-sync), session entry in plan/notes files.
- If the fix revealed a new gotcha, add it to this skill and the Notion runbook.
