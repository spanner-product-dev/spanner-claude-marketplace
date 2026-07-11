---
name: spanneros-schema-migration
description: >
  Writes safe, correctly-formatted SQL migration files for SpannerOS's Supabase Postgres database.
  Use whenever adding tables, columns, enum values, seed data, or constraints to SpannerOS —
  especially for writing 002_schema_updates.sql and any future numbered migration files. Triggers
  on: write the schema migration, add a column to [table], write 002_schema_updates, add the sm
  enum value, reseed billing_roles, create a new table for, add the is_billable flag, or any
  request involving ALTER TABLE, CREATE TABLE, ALTER TYPE, or schema changes in SpannerOS. Always
  invoke this skill before writing migration SQL — it encodes safe patterns for Supabase, the
  correct file numbering convention, and the style guide that must match 001_initial_schema.sql.
  Schema mistakes are expensive to undo once a Supabase project has live data.
---

# SpannerOS Schema Migration Writer

## Read the existing schema first — always

Before writing any SQL, read these files:

1. `/Users/mcurry/Documents/Claude/Projects/Spanner Planner and Time Management/SpannerOS/schema/001_initial_schema.sql`
   — List every table name, column, enum type and its values, RLS policy, and index.
2. Every additional migration file in `SpannerOS/schema/` beyond 001
   — Note what has already been applied so you don't duplicate it.

Confirm the current state of the schema before writing a single line. Guessing at column names or enum values is the most common source of migration errors.

---

## File naming convention

Migrations are sequential SQL files in `SpannerOS/schema/`:

```
001_initial_schema.sql    ← exists, do not touch
002_schema_updates.sql    ← next migration (write here)
003_...                   ← future
```

Name files with a short, descriptive suffix. Never edit `001_initial_schema.sql` — it's the historical baseline. All changes go in new numbered files.

---

## Safe patterns by operation type

### Adding an enum value

```sql
-- ALTER TYPE ... ADD VALUE is irreversible in Postgres.
-- Confirm spelling carefully — you cannot undo this.
ALTER TYPE user_role ADD VALUE 'sm';
```

This cannot be rolled back with a simple DROP. Double-check the exact value string before including it. Note it explicitly in a SQL comment so Mason can confirm before applying.

### Adding a column

```sql
-- Use IF NOT EXISTS so the migration is idempotent (safe to run twice).
-- New NOT NULL columns must have a DEFAULT to avoid locking the table.
ALTER TABLE billing_roles
  ADD COLUMN IF NOT EXISTS is_billable boolean NOT NULL DEFAULT true;

-- Nullable columns need no default.
ALTER TABLE project_billing_roles
  ADD COLUMN IF NOT EXISTS custom_name text,
  ADD COLUMN IF NOT EXISTS custom_rate numeric;
```

### Making an existing column nullable

```sql
ALTER TABLE project_billing_roles
  ALTER COLUMN billing_role_id DROP NOT NULL;
```

### Deleting and reseeding a lookup table

```sql
-- Safe for lookup tables with no live user data yet.
-- Use DELETE (not TRUNCATE) if child tables may have rows — DELETE respects FK constraints
-- and will fail loudly rather than silently cascade.
DELETE FROM billing_roles;

INSERT INTO billing_roles (name, default_rate, is_billable) VALUES
  ('CTO',                           350.00, true),
  ('Principal',                     300.00, true),
  ('Technical Program Lead',        275.00, true),
  ('Sr. Product Development',       250.00, true),
  ('Product Development',           175.00, true),
  ('Product Development - EE/FW',   175.00, true),
  ('NB - Technical Program Lead',   275.00, false),
  ('NB - Sr. Product Development',  300.00, false),
  ('NB - Product Development',      175.00, false)
;
```

### Creating a new table

```sql
CREATE TABLE IF NOT EXISTS user_billing_roles (
  user_id         uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  billing_role_id uuid NOT NULL REFERENCES billing_roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, billing_role_id)
);

-- Every new table needs RLS enabled.
ALTER TABLE user_billing_roles ENABLE ROW LEVEL SECURITY;

-- Add policies based on the access pattern.
-- Look at similar tables in 001_initial_schema.sql for the right template.
CREATE POLICY "Users can view their own billing roles"
  ON user_billing_roles FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Admins can manage all user billing roles"
  ON user_billing_roles FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE id = auth.uid() AND role = 'admin'
    )
  );
```

---

## What not to do

- **Never use `DROP TABLE` or `DROP COLUMN`** — destructive and irreversible; if removal is truly needed, discuss first
- **Never edit `001_initial_schema.sql`** — it is the historical record; changes go in new numbered files
- **Never skip RLS on a new table** — even lookup tables need it; Supabase exposes tables via the public API by default
- **Never use `TRUNCATE ... CASCADE`** on tables that might have live rows in child tables — use `DELETE` instead, which will fail loudly if FK constraints are violated
- **Never apply to Supabase without review** — show the full SQL and get approval first

---

## RLS policy patterns

When writing RLS for a new table, match the pattern used on the most similar table in `001_initial_schema.sql`. Common patterns:

- **User-scoped read**: `USING (user_id = auth.uid())`
- **Admin full access**: `USING (EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin'))`
- **Project member read**: `USING (EXISTS (SELECT 1 FROM project_users WHERE project_id = [table].project_id AND user_id = auth.uid()))`

If unsure which policy pattern fits, ask rather than guess — wrong RLS lets in data that shouldn't be visible.

---

## Output format

1. Write the complete SQL file with a header comment block identifying: migration number, date, and a summary of changes
2. Group changes into clearly commented sections (enums, table alterations, new tables, seed data)
3. Show the full SQL before saving to disk
4. State in plain English what each change does and flag any irreversible operations
5. Ask for explicit approval before writing the file

---

## Style guide (match `001_initial_schema.sql`)

- Section dividers: `-- ============================================================`
- Two blank lines between major sections
- Inline comments on non-obvious fields or constraints
- All names in `snake_case`
- Constraint names explicit: `fk_table_column`, `uq_table_column`
- Numeric amounts as `numeric(10,2)` for money, bare `numeric` for rates/multipliers
- Header comment block at top of file:

```sql
-- ============================================================
-- Migration: 002_schema_updates
-- Date: YYYY-MM-DD
-- Changes:
--   1. Add 'sm' value to user_role enum
--   2. Add is_billable to billing_roles
--   ...
-- ============================================================
```
