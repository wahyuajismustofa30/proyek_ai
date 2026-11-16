-- Conceptual notes only. Do not run this file as a production migration.
-- The canonical schema must be implemented in Prisma and versioned migrations.

-- Core:
-- users(id, email, display_name, password_hash, status, created_at, updated_at)
-- workspaces(id, name, slug, type, timezone, default_currency, status, created_by)
-- roles(id, workspace_id nullable, name)
-- permissions(id, code, description)
-- role_permissions(role_id, permission_id)
-- workspace_members(id, workspace_id, user_id, role_id, status, joined_at)
-- audit_logs(id, workspace_id, actor_user_id, action, resource_type,
--            resource_id, before_data jsonb, after_data jsonb, request_id, created_at)

-- Finance:
-- financial_entities(id, workspace_id, name, entity_type, currency, status)
-- accounts(id, financial_entity_id, name, account_type, opening_balance bigint)
-- categories(id, workspace_id, name, kind, parent_id)
-- journal_entries(id, workspace_id, financial_entity_id, entry_number,
--                 entry_date, description, status, created_by, posted_by,
--                 posted_at, reversal_of_id)
-- journal_lines(id, journal_entry_id, account_id, debit_amount bigint,
--               credit_amount bigint, category_id, memo)

-- Important posting invariant:
-- SUM(debit_amount) = SUM(credit_amount) for each posted journal entry.
-- Enforce in a server-side database transaction; consider a deferred
-- constraint trigger if strict database-level enforcement is required.
-- A journal line must not have both debit and credit positive.
-- Posted entries are corrected through reversal/adjustment, not silent edits.
