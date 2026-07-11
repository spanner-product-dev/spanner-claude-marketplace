---
name: spanneros-crud-scaffolder
description: >
  Scaffolds complete CRUD screens for SpannerOS — the Spanner PD internal web app built on
  Next.js App Router + TypeScript + Supabase + shadcn/ui + zod. Use this skill whenever building
  any new page, form, list view, detail view, or data entry screen for SpannerOS. Triggers on:
  build the clients page, scaffold the project list, create the intake wizard, build a CRUD screen
  for [entity], add the [entity] UI, implement Phase 2 screen, or any request to write SpannerOS
  frontend code. Always invoke this skill before writing any SpannerOS frontend code — it encodes
  the three-client Supabase pattern, App Router file conventions, and component structure that must
  be consistent across every screen. When in doubt, use this skill — off-pattern Supabase client
  usage causes silent auth bugs that are painful to trace.
---

# SpannerOS CRUD Scaffolder

## Read the schema first — always

Before writing a single line of code, read these files in order:

1. `/Users/mcurry/Documents/Claude/Projects/Spanner Planner and Time Management/SpannerOS/schema/001_initial_schema.sql`
   — List all table names and enum values out loud.
2. The most recent migration file in the same `SpannerOS/schema/` directory (if one exists beyond 001)
   — Note any new tables, columns, or enum values added since the initial schema.
3. `SpannerOS/docs/spanneros-schema-reference.md`
   — Skim the relevant tables for the screen being built: fields, relationships, RLS notes.

Name the tables the screen touches and confirm the field list before writing anything. Skipping this step risks generating code that references nonexistent columns or misses a foreign key.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js App Router, TypeScript, `src/` directory |
| Database + Auth | Supabase (Postgres + RLS + Auth) |
| Supabase client | `@supabase/ssr` — **three distinct clients** (see below) |
| UI components | shadcn/ui: button, card, dialog, form, input, select, table, sonner |
| Validation | zod |
| Mutations | Server Actions (`'use server'`) |

---

## The Three-Client Rule

This is the most important pattern in SpannerOS. Getting these wrong causes auth bugs that are invisible at build time and confusing at runtime.

| Client | File | Used in | Purpose |
|--------|------|---------|---------|
| Server client | `src/lib/supabase/server.ts` | Server Components, Server Actions, Route Handlers | Data fetching, mutations |
| Browser client | `src/lib/supabase/client.ts` | `"use client"` components | Client-side reads, realtime subscriptions |
| Middleware client | `src/lib/supabase/middleware.ts` | `middleware.ts` only | Session refresh — never for data queries |

**The rule is simple:** Server Components and Server Actions use the server client. Client Components use the browser client. Never cross them. When in doubt, look at an existing file in `src/lib/supabase/` to confirm the exact import path and instantiation pattern.

---

## File structure for a CRUD screen

Using `clients` as the example entity. Apply the same pattern for any entity.

```
src/app/(app)/clients/
├── page.tsx                  ← Server Component — fetches list, passes to table component
├── new/
│   └── page.tsx              ← Server Component — renders empty form
└── [id]/
    ├── page.tsx              ← Server Component — fetches single record, renders detail
    └── edit/
        └── page.tsx          ← Server Component — fetches record, renders pre-filled form

src/app/(app)/clients/_components/
├── clients-table.tsx         ← "use client" — sortable/filterable table
├── client-form.tsx           ← "use client" — create/edit form with validation
└── client-detail.tsx         ← "use client" — read-only detail view with edit button

src/app/(app)/clients/actions.ts   ← 'use server' — createClient, updateClient, deleteClient
src/lib/validations/clients.ts     ← zod schemas, inferred TypeScript types
```

---

## Standard code patterns

### Server Component (list page)

```typescript
// src/app/(app)/clients/page.tsx
import { createServerClient } from '@/lib/supabase/server'
import { ClientsTable } from './_components/clients-table'

export default async function ClientsPage() {
  const supabase = await createServerClient()
  const { data: clients, error } = await supabase
    .from('clients')
    .select('*')
    .order('name')

  if (error) throw error
  return <ClientsTable clients={clients ?? []} />
}
```

### Server Action (mutation)

```typescript
// src/app/(app)/clients/actions.ts
'use server'
import { createServerClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { clientSchema } from '@/lib/validations/clients'

export async function createClient(formData: FormData) {
  const supabase = await createServerClient()
  const parsed = clientSchema.safeParse(Object.fromEntries(formData))

  if (!parsed.success) return { error: parsed.error.flatten() }

  const { error } = await supabase.from('clients').insert(parsed.data)
  if (error) return { error: error.message }

  revalidatePath('/clients')
  return { success: true }
}
```

### zod validation schema

```typescript
// src/lib/validations/clients.ts
import { z } from 'zod'

export const clientSchema = z.object({
  name: z.string().min(1, 'Client name is required'),
  // add remaining fields from the table schema
})

export type ClientFormData = z.infer<typeof clientSchema>
```

### Client Component form

```typescript
// src/app/(app)/clients/_components/client-form.tsx
'use client'
import { useActionState } from 'react'
import { createClient } from '../actions'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Form, FormField, FormItem, FormLabel,
  FormControl, FormMessage,
} from '@/components/ui/form'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { clientSchema, type ClientFormData } from '@/lib/validations/clients'

export function ClientForm() {
  const form = useForm<ClientFormData>({
    resolver: zodResolver(clientSchema),
    defaultValues: { name: '' },
  })

  async function onSubmit(data: ClientFormData) {
    const formData = new FormData()
    Object.entries(data).forEach(([k, v]) => formData.append(k, String(v)))
    await createClient(formData)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Client Name</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Create Client</Button>
      </form>
    </Form>
  )
}
```

---

## Foreign key lookups

When a form has a foreign key field (e.g., `client_id` on a project), the parent list must be fetched server-side and passed as a prop:

```typescript
// In the page Server Component
const { data: clients } = await supabase.from('clients').select('id, name').order('name')
// Pass clients to the form component as a prop
// In the form, render a <Select> with shadcn/ui using the clients array
```

Don't fetch foreign key lists in a Client Component — that requires the browser client and adds unnecessary round-trips.

---

## RLS awareness

All tables have Row Level Security enabled. Queries run through Server Actions inherit the authenticated user's session, so RLS applies automatically. If a query returns fewer rows than expected, check whether the current user's role has the right SELECT policy on that table — look at the relevant policy in `001_initial_schema.sql`.

Never use the Supabase service role key in application code. That key bypasses RLS entirely and is only for migrations and scripts.

---

## Generating a new screen — checklist

1. Name the entity and identify which table(s) it reads and writes
2. List the form fields (from the schema) and their types/constraints
3. Identify any foreign key lookups needed and which table they come from
4. Note any enum fields — those become `<Select>` components with the enum values as options
5. Generate files in this order: zod schema → server actions → Server Component pages → Client Component files
6. After generating, list any manual steps needed (e.g., adding the route to the nav sidebar)

---

## Output rules

- Generate complete, runnable TypeScript — no `// TODO` stubs or placeholder comments
- If something is unclear (e.g., which columns to include in the list view), ask before guessing
- Use the exact file paths from the structure above
- Include all imports
- Keep components small and focused — a form component should not also fetch data
