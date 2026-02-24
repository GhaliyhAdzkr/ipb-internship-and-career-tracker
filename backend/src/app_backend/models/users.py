"""
Model: auth.users
Tabel pengguna utama dengan skema 'auth'.
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (Boolean, DateTime, Enum, String, UniqueConstraint,
                        Uuid, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.application_logs import ApplicationLogs
    from app_backend.models.auth_action_tokens import AuthActionTokens
    from app_backend.models.notification_queue import NotificationQueue
    from app_backend.models.user_refresh_tokens import UserRefreshTokens
    from app_backend.models.vacancies import Vacancies


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="users_email_key"),
        {"schema": "auth"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("public.gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("ADMIN", "STUDENT", name="user_role_enum", schema="auth"), nullable=False
    )
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    refresh_tokens: Mapped[list["UserRefreshTokens"]] = relationship(
        "UserRefreshTokens", back_populates="user", cascade="all, delete-orphan"
    )
    action_tokens: Mapped[list["AuthActionTokens"]] = relationship(
        "AuthActionTokens", back_populates="user", cascade="all, delete-orphan"
    )
    notification_queue: Mapped[list["NotificationQueue"]] = relationship(
        "NotificationQueue", back_populates="user"
    )
    vacancies: Mapped[list["Vacancies"]] = relationship(
        "Vacancies", back_populates="users"
    )
    application_logs: Mapped[list["ApplicationLogs"]] = relationship(
        "ApplicationLogs", back_populates="users"
    )

    # ---------- Domain helpers ----------

    def to_domain(self):
        """Convert ke domain model User"""
        from app_backend.domain.user import User as DomainUser
        from app_backend.domain.user import UserRole

        return DomainUser(
            id=self.id,
            email=self.email,
            password_hash=self.password_hash,
            role=self.role,
            is_active=self.is_active if self.is_active is not None else True,
            last_login_at=self.last_login_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, domain_user) -> "Users":
        """Buat ORM model dari domain User"""
        return cls(
            id=domain_user.id,
            email=domain_user.email,
            password_hash=domain_user.password_hash,
            role=domain_user.role,
            is_active=domain_user.is_active,
            last_login_at=domain_user.last_login_at,
            created_at=domain_user.created_at,
            updated_at=domain_user.updated_at,
        )
