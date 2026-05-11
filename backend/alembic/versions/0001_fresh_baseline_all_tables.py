"""Fresh baseline: Create all application tables from scratch

Revision ID: 0001_fresh_baseline_all_tables
Revises: None
Create Date: 2026-05-12 12:00:00.000000

This is a fresh baseline migration that creates all application tables
from the current SQLAlchemy model definitions. This replaces previous
incremental migrations (0001-0005) with a single comprehensive schema
creation for a clean Supabase migration.

To use this migration safely:
1. Delete old migration files (0001-0005) if starting completely fresh
2. Run: poetry run alembic upgrade head
3. This will create all tables from scratch

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_fresh_baseline_all_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables/types according to SQLAlchemy metadata.
    
    This uses the SQLAlchemy models as the single source of truth and
    issues CREATE statements for everything present in metadata.
    
    For Supabase compatibility:
    - All tables are in the public schema
    - UUID generation is handled by Python (sqlalchemy.dialects.postgresql.UUID)
    - pgcrypto extension is created but not strictly required
    """
    bind = op.get_bind()

    # Ensure required Postgres extensions exist
    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    except Exception:
        # pgcrypto might not be available, but it's optional
        # UUID generation will be handled on the application side
        pass

    # Import models metadata to ensure app path resolution
    from app_backend.models.base import Base

    # Create all tables, types, and indexes according to SQLAlchemy metadata
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    """Drop all application tables (destructive).
    
    Note: This will NOT drop Supabase's built-in auth tables in the auth schema.
    Only drops our application tables.
    """
    bind = op.get_bind()

    from app_backend.models.base import Base

    # Drop all application tables
    Base.metadata.drop_all(bind=bind)

    # Optionally drop our schema (but keep Supabase auth schema intact):
    # op.execute("DROP SCHEMA IF EXISTS public CASCADE;")
    # op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
