"""initial models

Revision ID: 0001_models_initial
Revises:
Create Date: 2026-03-03
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_models_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables/types according to SQLAlchemy metadata.

    This uses the SQLAlchemy models as the single source of truth and
    issues CREATE statements for everything present in metadata.

    Note: For complex Postgres-specific objects (custom schemas, enums
    in non-default schemas, triggers) you should verify the generated
    DDL on a test DB before applying to production.
    """
    bind = op.get_bind()

    # Ensure required Postgres extensions and schemas exist before creating types
    # and tables (SQLAlchemy will create ENUM types in their schema).
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    op.execute("CREATE SCHEMA IF NOT EXISTS auth;")

    # import models metadata here to ensure app path resolution
    from app_backend.models.base import Base

    # Create tables, types, indexes according to SQLAlchemy metadata
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()

    from app_backend.models.base import Base

    # drop_all will attempt to drop tables in metadata; use with caution
    Base.metadata.drop_all(bind=bind)

    # Optionally drop schema and extension (commented out as destructive):
    # op.execute("DROP SCHEMA IF EXISTS auth CASCADE;")
    # op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
