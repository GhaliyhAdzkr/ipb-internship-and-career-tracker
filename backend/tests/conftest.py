"""
Shared test fixtures and configuration.

Strategy:
- TestClient dari fastapi.testclient (sync, tidak perlu async)
- Tidak perlu koneksi DB nyata, test berjalan offline
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Generator
from unittest.mock import MagicMock

# Harus di-set SEBELUM import app agar lifespan tidak memanggil create_all
os.environ["TESTING"] = "1"

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app_backend.domain.student import Student as DomainStudent
from app_backend.domain.user import User as DomainUser
from app_backend.domain.user import UserRole
from app_backend.main import app
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import (get_current_active_student,
                                             get_current_active_user,
                                             get_current_student,
                                             get_current_user, require_admin,
                                             require_student)

# ─── Fixed IDs used across tests ─────────────────────────────────────────────

STUDENT_USER_ID = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
ADMIN_USER_ID = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
DEPT_ID = uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")
SKILL_ID = uuid.UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")
COMPANY_ID = uuid.UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee")

NOW = datetime(2026, 2, 24, 12, 0, 0, tzinfo=timezone.utc)


# ─── Domain user stubs ────────────────────────────────────────────────────────


def make_student_user() -> DomainUser:
    return DomainUser(
        id=STUDENT_USER_ID,
        email="student@ipb.ac.id",
        password_hash="$2b$12$xxx",
        role=UserRole.STUDENT.value,
        is_active=True,
        last_login_at=NOW,
        created_at=NOW,
        updated_at=NOW,
    )


def make_student_domain() -> DomainStudent:
    """Create Student domain object for wishlist tests."""
    return DomainStudent(
        user_id=STUDENT_USER_ID,
        nim="G1234567890",
        full_name="Windah Basudara",
        semester=5,
        department_id=DEPT_ID,
        gpa=None,
        phone_number="+6281234567890",
        linkedin_url="https://linkedin.com/in/budi",
        cv_url="https://example.com/cv.pdf",
        is_mbkm_eligible=True,
        updated_at=NOW,
    )


def make_admin_user() -> DomainUser:
    return DomainUser(
        id=ADMIN_USER_ID,
        email="admin@ipb.ac.id",
        password_hash="$2b$12$xxx",
        role=UserRole.ADMIN.value,
        is_active=True,
        last_login_at=NOW,
        created_at=NOW,
        updated_at=NOW,
    )


# ─── Session mock factory ─────────────────────────────────────────────────────


def make_mock_session() -> MagicMock:
    """Return a fresh MagicMock that mimics a SQLAlchemy Session."""
    session = MagicMock()
    # Configura chain: session.query(...).filter(...).first() → None by default
    session.query.return_value.filter.return_value.first.return_value = None
    session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
        None
    )
    session.query.return_value.options.return_value.filter.return_value.first.return_value = (
        None
    )
    session.query.return_value.order_by.return_value.all.return_value = []
    return session


def get_mock_session() -> Generator:
    yield make_mock_session()


# ─── Pytest fixtures ──────────────────────────────────────────────────────────


@pytest.fixture
def mock_session() -> MagicMock:
    return make_mock_session()


@pytest.fixture
def client_no_auth(mock_session) -> Generator[TestClient, None, None]:
    """TestClient with only the DB session overridden (no auth)."""
    app.dependency_overrides[get_session] = lambda: mock_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def client_as_student(mock_session) -> Generator[TestClient, None, None]:
    """TestClient authenticated as a STUDENT."""
    student = make_student_user()
    student_domain = make_student_domain()
    app.dependency_overrides[get_session] = lambda: mock_session
    app.dependency_overrides[get_current_user] = lambda: student
    app.dependency_overrides[get_current_active_user] = lambda: student
    app.dependency_overrides[get_current_student] = lambda: student_domain
    app.dependency_overrides[get_current_active_student] = lambda: student_domain
    app.dependency_overrides[require_student] = lambda: student
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def client_as_admin(mock_session) -> Generator[TestClient, None, None]:
    """TestClient authenticated as an ADMIN."""
    admin = make_admin_user()
    app.dependency_overrides[get_session] = lambda: mock_session
    app.dependency_overrides[get_current_user] = lambda: admin
    app.dependency_overrides[get_current_active_user] = lambda: admin
    app.dependency_overrides[require_admin] = lambda: admin
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def client_as_admin_for_student_only(mock_session):
    admin = make_admin_user()

    async def _forbidden_student_dep():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak. Hanya STUDENT.",
        )

    app.dependency_overrides[get_session] = lambda: mock_session
    app.dependency_overrides[get_current_user] = lambda: admin
    app.dependency_overrides[get_current_active_user] = lambda: admin
    app.dependency_overrides[require_admin] = lambda: admin
    app.dependency_overrides[get_current_active_student] = _forbidden_student_dep

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
