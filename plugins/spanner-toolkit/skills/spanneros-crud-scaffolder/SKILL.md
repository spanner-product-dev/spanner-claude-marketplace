---
name: spanneros-crud-scaffolder
description: >
  Builds screens for SpannerOS — the Spanner PD internal planner, on Next.js App Router +
  TypeScript + Supabase + zod, with NO component library. Use whenever writing any page, form,
  list, detail view or table for the app. Triggers on: build the clients page, scaffold the
  project list, add a form for [entity], add a column to [screen], make this table sortable,
  build the [entity] UI, or any request to write SpannerOS frontend code. Invoke it BEFORE
  writing code: it encodes the real file layout (there is no `src/`), the native-form pattern
  (there is no shadcn/ui), the three Supabase clients, the two-place authorization rule, how
  money and project-scoped rows must be read, and the gotchas that have cost this project time.
---

# SpannerOS screens

**Rewritten 2026-09-15.** The previous version described a codebase that does not exist — a
`src/` tree, shadcn/ui, react-hook-form — and opened by telling the reader to load a file path
dead since the project folder was flattened. Everything below was read out of the repository.

---

## Read first

Repo: `~/Developer/spanner-planner`. Schema: `schema/001_initial_schema.sql` for the baseline,
then the later migrations for what changed (the sequence runs past `037`; there is no `015`).
Table inventory: `…/Projects/SpannerOS/specs/spanneros-schema-reference.md`.

Name the tables a screen touches and confirm the columns before writing. Guessing a column name
is the most common way this goes wrong, and `select *` hides it until runtime.

---

## The stack, as it actually is

| Layer | What |
|---|---|
| Framework | Next.js **16** App Router, TypeScript. **No `src/` directory** — routes live at `app/` |
| Route group | `app/(planner)/…` |
| Database + auth | Supabase (Postgres + RLS + Auth), `@supabase/ssr` |
| Validation | zod, parsing `FormData` directly |
| Mutations | Server Actions (`'use server'`) |
| UI | **Nothing.** No shadcn/ui, no react-hook-form, no component kit. Native elements and Tailwind classes |

Dependencies are `@supabase/ssr`, `@supabase/supabase-js`, `next`, `react`, `react-dom`, `xlsx`,
`zod`. If a pattern needs anything else, it is the wrong pattern.

---

## The native form pattern

Forms post straight to a server action. This is the decision on record and every screen follows
it — it is why there is no form library.

```tsx
// app/(planner)/clients/client-form.tsx
'use client'
export function ClientForm({ error }: { error?: string }) {
  return (
    <form action={createClient} className="grid max-w-xl gap-4">
      <label htmlFor="name" className="flex flex-col gap-1 text-sm">
        <span className="font-medium">Client name</span>
        <input id="name" name="name" required className="rounded border px-3 py-2" />
      </label>
      <button type="submit" className="rounded bg-black px-3 py-1.5 text-sm text-white">Save</button>
    </form>
  )
}
```

A client component is a **sibling file** (`client-form.tsx`, `team-table.tsx`), not a
`_components/` folder. Where a form lives in a dialog and needs its result inline rather than a
redirect, the action takes `(_prev, formData)` and the component uses `useActionState` — see
`createClientInline`.

### File layout for an entity

```
app/(planner)/clients/
├── page.tsx              Server Component — fetches the list
├── new/page.tsx          Server Component — renders the form
├── [id]/edit/page.tsx    Server Component — fetches one, renders a prefilled form
├── actions.ts            'use server' — create / update, zod-validated
├── client-form.tsx       'use client' — the form
└── import/ + import-actions.ts   where CSV import exists
```

---

## The three Supabase clients

| Client | File | Used in |
|---|---|---|
| Server | `lib/supabase/server.ts` → `createClient()` (**async — await it**) | Server Components, Server Actions |
| Browser | `lib/supabase/client.ts` → `createClient()` | `'use client'` components |
| Middleware | `lib/supabase/middleware.ts` → `updateSession()` | `proxy.ts` only — never for data |

Never cross them. **Naming trap:** `createClient` is also the name of the *server action* that
creates a client company (`app/(planner)/clients/actions.ts`). Read the import before assuming
which one is in scope.

In practice most screens do not touch Supabase from the browser at all: fetch in the server
component, flatten, and pass plain props down.

---

## Authorization goes in two places, every time

**The action calls `requireRole`, and the page calls it too** — `lib/auth.ts` gives you
`getProfile()`, `requireRole(allowed, redirectTo)` and `requireUser()`.

```ts
// Mirrors the clients_write RLS policy (admin + tpl). Kept here so the gate is
// visible in the action and not only buried in the database.
const CLIENT_WRITE_ROLES = ['admin', 'tpl'] as const

export async function createClient(formData: FormData) {
  const { supabase } = await requireRole([...CLIENT_WRITE_ROLES],
    `/clients?error=${encodeURIComponent('You do not have permission to create clients.')}`)
  …
}
```

The `allowed` list **mirrors that table's `*_write` RLS policy**, and a comment says so. RLS is
the real boundary and stays the backstop; the explicit gate gives a clean redirect instead of a
raw Postgres error, and lets the list page hide affordances the user cannot use.

Resolve the caller through **`users.auth_user_id`, never `users.id`** — `getProfile()` is the one
place that lookup lives. People exist without logins (contractors), so `public.users.id` is
self-generated and any lookup keyed on it matches nothing or the wrong row.

---

## Rows are project-scoped now — and money is not a UI concern

Since migrations 032–037, a person with `visibility_scope = 'assigned'` sees only projects they
are granted, **names included**. Two consequences for any screen:

- **Do not re-implement the rule.** RLS already filters; a query returning fewer rows than
  expected is usually correct. Never add a "show everything" path.
- **A refused write is a real outcome.** RLS rejection surfaces as a raw Postgres string — catch
  it and say something a person can act on.
- **Totals a scoped person sees cover their granted projects only.** Label them that way rather
  than silently showing a smaller number; someone's own hours under-reporting reads as a payroll
  error.

**Money never comes from a table read.** Rates, budgets and planned amounts come from the
`security definer` accessors, via RPC:

```ts
const [budgets, rates] = await Promise.all([
  supabase.rpc('money_project_budgets', { p_project_ids: [id] }),
  supabase.rpc('money_slot_rates', { p_project_id: id }),
])
```

They return nothing to a caller who may not see money, so an empty result is an answer, not an
error — but **throw rather than writing zeros** if slots that exist come back empty, because
planned amounts are computed from those rates. Never use the service-role key in app code.

---

## Reading embedded relations

PostgREST returns an embedded relation as an object or an array depending on the shape of the
join, so every file that uses one carries this helper:

```ts
function rel<T>(v: unknown): T | null {
  if (v == null) return null
  if (Array.isArray(v)) return (v[0] as T) ?? null
  return v as T
}
```

Display names go through helpers, never raw columns: `personDisplayName(u)` (first+last, falling
back to full name, then email) and `clientDisplayName(c)` (`code_name ?? name` — some clients are
confidential and their real name must never render).

---

## Tables: what a good one does here

The team list is the current reference (`app/(planner)/team/`). A list screen of any size wants:

- **Status visible and a sensible default filter.** `/team` was 111 rows of which 89 were
  inactive people shown with nothing to mark them — which is why two pairs read as duplicate
  records. Default to active, say what is hidden (`22 of 111 · 89 inactive hidden`).
- Sortable headers, a text filter, and a column chooser where the table has more fields than fit.
- Preferences in `localStorage`, **every access wrapped in try/catch** — blocked site data throws
  rather than returning null, and an unusable table is a poor trade for remembering a sort order.
- The server component flattens the PostgREST shape and passes plain rows; the client component
  has no business knowing how an embedded relation is spelled.

---

## Gotchas that have cost time

- **An unchecked checkbox is absent from `FormData`**, not `false`. The idiom in use:
  `z.union([z.literal('on'), z.null(), z.undefined()]).transform(v => v === 'on')`.
- **Never run `next build` while `next dev` is running** — they share `.next` and the dev server
  floods with RSC "Load failed" errors that look like a code bug. Use `npx tsc --noEmit`.
- **Dates are UTC in `lib/planning`.** `toISODate(new Date())` is a day early on Pacific; use
  local components for anything meaning "today".
- **A missing GRANT reads as `permission denied for table`** before RLS is evaluated — it is not
  an RLS problem and no policy change will fix it.
- Verify in the browser through **`/dev-enter`**, which mints a staging session (it 404s against
  prod by construction). Everything drives except the canvas grid editor, which does not accept
  synthetic keystrokes — grid edits need a human.

---

## Before you finish

1. `npx tsc --noEmit` — clean.
2. Drive the screen through `/dev-enter` and check the thing you claimed, not just that it
   renders. Counts, filters, an actual write.
3. Check it at 375px: no page-level horizontal scroll; tables scroll in their own container.
4. Say what is still manual — a nav entry, a migration that has to land first, a column nothing
   populates yet.

Generate complete, runnable TypeScript. No `// TODO` stubs. If something is genuinely ambiguous —
which columns belong in a list, what a filter should default to — ask rather than guess; this
codebase has a house style and guessing at it produces code that looks fine and reads wrong.
