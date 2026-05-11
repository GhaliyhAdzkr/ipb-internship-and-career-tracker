"""
Database configuration dan session management
Konfigurasi koneksi database dan session SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_backend.conf.settings import settings

SQLALCHEMY_DATABASE_URL = settings.db_url
SQLALCHEMY_DATABASE_TEST_URL = settings.db_test_url

# Use SQLAlchemy 2.0 style engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    pool_pre_ping=True,  # Verifikasi koneksi sebelum digunakan
    pool_recycle=3600,  # Recycle koneksi setiap 1 jam
)

SessionLocal = sessionmaker(
    autocommit=settings.session_auto_commit,
    autoflush=settings.session_auto_flush,
    bind=engine,
    future=True,
)

# Re-use the project's Declarative Base (defined in app_backend.models.base)
# This prevents having two different Base classes which can confuse Alembic
# and model imports.
# Base is imported above from app_backend.models.base


def get_session():
    """Dependency untuk mendapatkan database session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_database_url() -> str:
    """Get database URL untuk task workers"""
    return SQLALCHEMY_DATABASE_URL
