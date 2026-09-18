---
name: spanneros-schema-migration
description: >
  Writes, verifies and applies SQL migrations for the SpannerOS planner database (Supabase
  Postgres, shared with two other projects). Use whenever adding or altering tables, columns,
  enum values, constraints, RLS policies, functions or seed data — and whenever writing the
  verification script that must ship with them. Triggers on: write the migration, add a column
  to [table], add an RLS policy, change who can see [thing], write the verify script, apply to
  staging, why is this query slow, or any request involving ALTER TABLE, CREATE TABLE, CREATE
  POLICY, ALTER TYPE or GRANT in SpannerOS. Invoke it BEFORE writing any SQL: it encodes the
  numbering rule, the verify-script contract, the RLS performance rules, and the split between
  what Claude does and what Mason runs. Schema mistakes are expensive once a database has live
  data, and this project has paid for every rule in here.
---

# SpannerOS schema migrations

**Rewritten 2026-09-15** after the project-scoped visibility build (migrations 032–037), which
produced every rule below. The previous version pointed at a path that no longer exists and knew
nothing about verification scripts.

---

## Where things are

| | |
|---|---|
| **SQL of record** | `~/Developer/spanner-planner/schema/` — tracked in git, and the definition of both databases' state |
| **Working copy** | `…/Projects/SpannerOS/schema/` in Drive. Authored here, copied to the repo. **Keep them in step; nothing enforces it** |
| **What is applied where** | `schema/README.md`. It is the source of truth — do not restate it in the plan or the architecture file, both have been wrong |
| **Staging** | `cutkctzmojpgbwtoaiic` |
| **Prod** | `lyerknxfxesoecmpipip` — **never without an explicit go-ahead** |

Read the current schema before writing a line: `001_initial_schema.sql` for the baseline, then
the later files for what has changed. Guessing at a column name or enum value is the most common
way these go wrong.

Three files in `schema/` belong to the **matrix** project (`003`, `004`, `005`) and one to CRM.
They share the database, not the sequence. Never treat them as the planner's next number.

---

## The numbering rule

**A number belongs to the migration that lands. A parked spec holds no reservation.**
`program_review_notes` has now been penciled in for `027`, `029`, `030`, `031`, `032`, `033` and
`034`, and lost every one. `015` was never written — the sequence runs `014` → `016`.

**Re-check `schema/` immediately before claiming a number.** Numbers have been claimed on
unmerged branches before.

---

## Writing the migration

Match the house style, which is heavy on explanation because these files get read years later by
someone deciding whether they may change something.

- A header block stating **purpose, what is deliberately NOT in here, destructive or reversible,
  idempotent or not, what it depends on, the numbering note, and the apply order.**
- `create table if not exists`, `add column if not exists`, `create or replace function`, every
  policy dropped before it is created. A migration that cannot be run twice will be run twice.
- **Every new table needs RLS *and* a GRANT.** RLS decides which rows; the GRANT decides whether
  the role may touch the table at all, and a missing one reads as `permission denied for table`
  *before* RLS is evaluated. Grant `authenticated` and `service_role`, never `anon`, and list
  tables explicitly — no `ALL TABLES IN SCHEMA`, because two other projects live here.
- **`for all` with no `with check` reuses `using` as the insert check.** That reads as complete
  and is not; it is how `time_entries` came to allow a member to write against any slot in the
  database. Write the pair explicitly.
- Prefer a **CHECK constraint over an enum** for a small value set. A CHECK can be widened *and*
  narrowed; an enum label can never be dropped. Migration 032 chose a CHECK on that argument and
  033 widened it the next day.
- A new column with `NOT NULL` needs a DEFAULT, and the default decides who is affected on
  arrival. Default to the value that changes nothing.
- Introspect constraints with `pg_catalog.pg_constraint`, never
  `information_schema.constraint_column_usage` — it silently returns nothing for some FKs, and a
  check written the same way as the thing it checks reports a false PASS.
- **Never `DROP TABLE` / `DROP COLUMN`, and never `TRUNCATE … CASCADE`.** Use `DELETE`, which
  fails loudly against FK constraints instead of quietly taking children with it.

---

## RLS performance — the rules, with the numbers

A policy predicate is evaluated **per row**, and a `security definer` function **cannot be
inlined by the planner**. Putting one in a predicate is a cliff, not a slope:

| Same query, 767 rows out | |
|---|---|
| RLS off | 0.63 ms |
| `can_see_project(project_id)` per row | **195 ms** |
| the rule hoisted into a set | 39.7 ms |
| identity helpers wrapped as `(select f())` | **3.4 ms** |

```sql
-- row scoping: a set the planner builds once per statement, then hash-probes
using ( project_id in (select v from public.visible_project_ids() v) )

-- identity: a scalar subquery forces one InitPlan instead of a call per row
using ( user_id = (select public.current_user_id()) )
```

The point-check form survives for `with check` clauses and inside definer functions, where it
answers once. That leaves the rule written twice — so **a gate must assert the two spellings
agree**, rather than trusting them to.

**Measure before claiming.** Migration 034's own header said the per-row cost was "very likely
fine", gave three plausible reasons, and was 300× out. An `EXPLAIN (ANALYZE)` takes four minutes.

---

## The verify script — one per migration, no exceptions

`verify-0NN-<name>.sql`, and it is the other half of the deliverable.

**The contract:**

- One transaction ending in **`ROLLBACK`**, so it is safe against a live database.
- **A negative control first**, proving the harness can do the thing the other gates assert
  fails. If G0 failed, everything below it is green for the wrong reason.
- Every gate records a `PASS`/`FAIL` line **and the script `SELECT`s them back at the end** —
  `supabase db query` swallows `NOTICE`, which would reduce a fourteen-gate run to "it didn't
  error".
- **Never raise on failure.** Raising discards the evidence; a failing run is identified by its
  FAIL lines and its tally.
- Impersonate with `set_config('request.jwt.claims', …)` + `set local role authenticated` — what
  PostgREST does per request. Borrow a real user with a linked login and change their role inside
  the transaction; a synthetic `public.users` row cannot work, because `auth_user_id` is an FK to
  `auth.users`.
- When a migration is meant to change **nothing** on arrival, **assert that** — inertness is
  exactly the kind of claim that decays silently.

### Write gates that assert behaviour, not something adjacent

Four false failures in one day, all this mistake:

| The gate said | What it actually asserted | The fix |
|---|---|---|
| "studio regression, 74437/74436" | a count taken **before** the script planted its own row | census after every write — and note RLS can only *restrict*, so seeing MORE rows than the owner is impossible as a regression |
| "16 tables have no scope filter" | one **spelling** of the rule, after a refactor legitimately respelled it | accept every valid spelling, or assert the rule's effect |
| "still takes 20.6 ms" | a **cold cache** on first call; the real figure was 3.2 ms warm | warm it, run twice and use the second, and compare against a **control** (a raw scan of the same table) rather than a constant someone typed |
| "carries 1.50 logged hours" | "any hours **ever**" — a locked 2021 row no screen can render | scope the question to the window the surface actually renders |
| "work with no project is refused" | **one of the two ways** it is refused — the gate caught `check_violation`, but the trigger raises P0001 and gets there first, so the exception escaped and aborted the whole run on a correct migration | catch `others` and record the SQLSTATE: assert THAT the write was refused, print HOW |

A gate that cries wolf is one people learn to skip, and then it is not a gate.

---

## Checking SQL before it reaches a database

There is no local Postgres. Parse it offline — this catches the typo that otherwise fails halfway
through a migration in the SQL editor:

```
npm install pgsql-parser libpg-query      # in a scratch dir, NEVER in Drive
```

```js
import { parse } from 'pgsql-parser'
import { parsePlPgSQL } from 'libpg-query'
await parse(sql)          // top-level statements
await parsePlPgSQL(sql)   // the bodies inside $$ … $$, which parse() sees as strings
```

**Both halves matter:** `parse()` alone reports OK on a `do $$ … $$` block whose plpgsql is
malformed. Verify the harness against deliberate errors in both positions before trusting it. It
is a syntax check and nothing more — it cannot see a missing GRANT or an upsert that needs
table-level SELECT.

---

## Applying — who does what

**Claude writes, parse-checks and probes read-only. Mason applies.** In auto mode the write is
refused by the permission classifier as a DDL write to a live database, and that split has held
through every migration. Do not ask for a permission grant; hand over the commands.

Read-only queries **do** run, including a `begin; … rollback;` probe that impersonates a user.
Use them to check preconditions before handing anything over.

One command per block:

```bash
cat ~/Developer/spanner-planner/supabase/.temp/project-ref
```

It must print the staging ref. **Both projects show a `main PRODUCTION` badge in the dashboard
and that badge is the branch, not the environment** — the ref is the only reliable signal.

```bash
cd ~/Developer/spanner-planner && supabase db query --linked -f schema/0NN_name.sql
```

```bash
cd ~/Developer/spanner-planner && supabase db query --linked -f schema/verify-0NN-name.sql
```

Then **confirm from the catalogue, not from the run output** — query `pg_policies`,
`information_schema.columns`, `pg_proc` and watch the thing exist. A verify script that passes is
still the script grading its own homework.

**This is not belt-and-braces.** On 2026-09-18, `supabase db query` applied migration 042, printed
no error, and had created a second `save_break` overload instead of replacing one *and* left `anon`
able to execute it. Both were invisible in the run output and obvious in `pg_proc` — two rows where
there should have been one, and a `has_function_privilege('anon', …)` of true. A clean exit means
the statements parsed and ran; it says nothing about whether they did what the file claims.

If a project seems unreachable, `supabase projects list` is read-only and shows whether it has
auto-paused, which has been the cause before.

---

## Three lessons that cost real time

**A privilege change is not verified by a read test.** Migration 025's read half was dry-run
tested and worked; its write half was never exercised until a human clicked Save, by which point
it was in prod. `insert … on conflict do update` needs **table-level** SELECT, which column
grants do not satisfy, and it fails as `permission denied for table <t>` — which reads like a
missing grant and is not.

**`create or replace function` KEYS ON THE SIGNATURE — change the arguments and you have
created a second function, not replaced one.** Migration 042 added one defaulted argument to
`save_break` and left 039's version sitting beside it, still enforcing the rule 042 existed to
lift. PostgREST calls by NAMED arguments and both overloads accepted the same five names, so the
call was ambiguous; in plain SQL the exact-arity match wins, which is the old one. **And the new
function was executable by `anon`** — a newly created function is executable by `PUBLIC` by
default, and the `revoke` that 039 had applied belongs to the OLD signature. That half is silent:
nothing errors, the function simply becomes reachable without a session.

So: `drop function if exists <old exact signature>` beside the create, and **re-state the grants
whenever a signature is new** — `revoke all … from public, anon; grant execute … to authenticated,
service_role;`. **A function's ACL belongs to its signature.** Assert it in the verify script too
(count the overloads, and check `has_function_privilege('anon', …)`), because neither symptom
raises. Migration 031 had already written the grant half down — "the grants are re-applied below,
since they do not survive" — and 042 did not read it.

**A return-type change has the blast radius of every consumer.** 031 changed `close_block`'s
return type; a verify script declared the old one and `select * into` mapped the new composite
*positionally*, pushing a `date` into a `uuid` column. PL/pgSQL does not warn. Grep for consumers
first.

---

## Afterwards

- Copy the file to **both** locations (repo + Drive) and say so.
- Update `schema/README.md`'s applied-where table and the prod backlog.
- Update the numbering line in `CLAUDE.md` and `plan-spanneros.md` — next free number, staging
  state, what prod owes and **in what order** (some must follow others; say which, and say when
  one is not optional).
- A durable rule goes in `architecture-spanneros.md` only if it constrains more than one module;
  otherwise `modules/<surface>.md`. Narrative goes to `history/YYYY-MM.md`.
