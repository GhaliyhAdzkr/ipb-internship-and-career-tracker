"""add activate_account to auth_action_enum

Revision ID: 0005_add_activate_account
Revises: 4f63b6d2fdcb
Create Date: 2026-05-07 21:24:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0005_add_activate_account"
down_revision = "4f63b6d2fdcb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Postgres Enum modification cannot be done in a transaction in some versions
    # We use op.execute with autocommit for safety
    op.execute("COMMIT") # End current transaction
    op.execute("ALTER TYPE auth.auth_action_enum ADD VALUE 'ACTIVATE_ACCOUNT'")


def downgrade() -> None:
    # Downgrading enums in Postgres is complex (requires recreating the type)
    # For a dev migration, we can leave it or skip it
    pass
