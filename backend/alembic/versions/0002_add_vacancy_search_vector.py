
"""add_vacancy_search_vector

Revision ID: 86162200e497
Revises: 0001_fresh_baseline_all_tables
Create Date: 2026-05-12 14:37:19.624599
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '86162200e497'
down_revision = '0001_fresh_baseline_all_tables'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add search_vector column
    op.add_column('vacancies', sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True))
    
    # 2. Create GIN index
    op.create_index('idx_vacancies_search_vector', 'vacancies', ['search_vector'], unique=False, postgresql_using='gin')

    # 3. Create Trigger Function
    op.execute("""
        CREATE OR REPLACE FUNCTION vacancies_search_vector_update() RETURNS trigger AS $$
        begin
          new.search_vector :=
             setweight(to_tsvector('indonesian', coalesce(new.title,'')), 'A') ||
             setweight(to_tsvector('indonesian', coalesce(new.description,'')), 'B');
          return new;
        end
        $$ LANGUAGE plpgsql;
    """)

    # 4. Create Trigger
    op.execute("""
        CREATE TRIGGER vacancies_search_vector_trigger BEFORE INSERT OR UPDATE
        ON vacancies FOR EACH ROW EXECUTE FUNCTION vacancies_search_vector_update();
    """)

    # 5. Sync existing data
    op.execute("""
        UPDATE vacancies SET search_vector = 
            setweight(to_tsvector('indonesian', coalesce(title,'')), 'A') || 
            setweight(to_tsvector('indonesian', coalesce(description,'')), 'B');
    """)


def downgrade():
    # 1. Drop trigger
    op.execute("DROP TRIGGER IF EXISTS vacancies_search_vector_trigger ON vacancies")
    
    # 2. Drop function
    op.execute("DROP FUNCTION IF EXISTS vacancies_search_vector_update")
    
    # 3. Drop index
    op.drop_index('idx_vacancies_search_vector', table_name='vacancies', postgresql_using='gin')
    
    # 4. Drop column
    op.drop_column('vacancies', 'search_vector')
