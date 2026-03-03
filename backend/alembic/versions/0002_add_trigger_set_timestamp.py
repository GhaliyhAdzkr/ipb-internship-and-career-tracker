"""add trigger_set_timestamp function and triggers

Revision ID: 0002_add_trigger_set_timestamp
Revises: 0001_models_initial
Create Date: 2026-03-03
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_add_trigger_set_timestamp"
down_revision = "0001_models_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the trigger function in public schema
    op.execute(
        """
        CREATE OR REPLACE FUNCTION public.trigger_set_timestamp()
        RETURNS trigger
            LANGUAGE plpgsql
            AS $$
        BEGIN
          NEW.updated_at = NOW();
          RETURN NEW;
        END;
        $$;
        """
    )

    # Ensure auth schema exists (some deployments may have created it earlier)
    op.execute("CREATE SCHEMA IF NOT EXISTS auth;")

    # Attach triggers for tables that use updated_at column
    triggers = [
        ("auth", "user_refresh_tokens", "set_timestamp_user_refresh_tokens"),
        ("auth", "users", "set_timestamp_users"),
        ("public", "profiles_admin", "set_timestamp_admin"),
        ("public", "applications", "set_timestamp_applications"),
        ("public", "placements", "set_timestamp_placements"),
        ("public", "profiles_student", "set_timestamp_student"),
        ("public", "vacancies", "set_timestamp_vacancies"),
    ]

    for schema, table, trigger_name in triggers:
        # drop existing trigger if present, then create
        op.execute(f"DROP TRIGGER IF EXISTS {trigger_name} ON {schema}.{table};")
        op.execute(
            f"CREATE TRIGGER {trigger_name} BEFORE UPDATE ON {schema}.{table} FOR EACH ROW EXECUTE FUNCTION public.trigger_set_timestamp();"
        )


def downgrade() -> None:
    triggers = [
        ("auth", "user_refresh_tokens", "set_timestamp_user_refresh_tokens"),
        ("auth", "users", "set_timestamp_users"),
        ("public", "profiles_admin", "set_timestamp_admin"),
        ("public", "applications", "set_timestamp_applications"),
        ("public", "placements", "set_timestamp_placements"),
        ("public", "profiles_student", "set_timestamp_student"),
        ("public", "vacancies", "set_timestamp_vacancies"),
    ]

    for schema, table, trigger_name in triggers:
        op.execute(f"DROP TRIGGER IF EXISTS {trigger_name} ON {schema}.{table};")

    # Optionally remove the function; keep it if other code relies on it
    op.execute("DROP FUNCTION IF EXISTS public.trigger_set_timestamp();")
