"""add_users_username

Revision ID: 30162200e498
Revises: 86162200e497
Create Date: 2026-05-18 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30162200e498'
down_revision = '86162200e497'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add username column as nullable first to allow seamless population
    op.add_column('users', sa.Column('username', sa.String(length=100), nullable=True))
    
    # 2. Populate username column for all existing users using email prefix
    op.execute("UPDATE users SET username = split_part(email, '@', 1);")
    
    # 3. Add unique constraint on the username column
    op.create_unique_constraint('uq_users_username', 'users', ['username'])


def downgrade():
    # 1. Drop unique constraint
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    
    # 2. Drop username column
    op.drop_column('users', 'username')
