"""
Domain Model untuk User
Selaras dengan skema DB: hanya role ADMIN dan STUDENT.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"

    @classmethod
    def values(cls) -> list[str]:
        return [r.value for r in cls]


@dataclass
class User:
    """Pure domain model untuk User, berisi business logic tanpa ORM dependency."""

    id: uuid.UUID
    email: str
    password_hash: str
    role: str  # nilai dari UserRole enum
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validasi domain invariants."""
        if not self.email or "@" not in self.email:
            raise ValueError("Alamat email tidak valid")

        if self.role not in UserRole.values():
            raise ValueError(
                f"Role tidak valid: '{self.role}'. "
                f"Role yang diizinkan: {UserRole.values()}"
            )

        now = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

    # ---------- State transitions ----------

    def activate(self) -> None:
        """Aktifkan akun user."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Nonaktifkan akun user (soft-disable)."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def record_login(self) -> None:
        """Catat waktu login terakhir."""
        now = datetime.now(timezone.utc)
        self.last_login_at = now
        self.updated_at = now

    # ---------- Role predicates ----------

    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT.value

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN.value
