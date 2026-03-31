"""rename refresh_token to token_hash in user_refresh_tokens

Revision ID: 0003_fix_refresh_tokens
Revises: 0002_add_trigger_set_timestamp
Create Date: 2026-03-31
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0003_fix_refresh_tokens"
down_revision = "0002_add_trigger_set_timestamp"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename column `refresh_token` -> `token_hash` in auth.user_refresh_tokens
    op.alter_column(
        "user_refresh_tokens",
        "refresh_token",
        new_column_name="token_hash",
        schema="auth",
    )

    # Also add a unique constraint on token_hash if not already present
    # (the ORM model defines unique=True on the column)
    op.create_unique_constraint(
        "uq_user_refresh_tokens_token_hash",
        "user_refresh_tokens",
        ["token_hash"],
        schema="auth",
    )

    # Drop old updated_at column that doesn't exist in current ORM model
    op.drop_column("user_refresh_tokens", "updated_at", schema="auth")


def downgrade() -> None:
    op.add_column(
        "user_refresh_tokens",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        schema="auth",
    )

    op.drop_constraint(
        "uq_user_refresh_tokens_token_hash",
        "user_refresh_tokens",
        schema="auth",
        type_="unique",
    )

    op.alter_column(
        "user_refresh_tokens",
        "token_hash",
        new_column_name="refresh_token",
        schema="auth",
    )
