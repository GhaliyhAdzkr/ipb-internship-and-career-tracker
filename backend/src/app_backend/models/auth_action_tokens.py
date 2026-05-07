"""
Model: auth.auth_action_tokens
Tabel untuk one-time action tokens (reset password, aktivasi akun, dan lain-lain).
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKeyConstraint, Index, String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.users import Users


class AuthActionTokens(Base):
    __tablename__ = "auth_action_tokens"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
            ondelete="CASCADE",
            name="auth_action_tokens_user_id_fkey",
        ),
        Index(
            "idx_action_tokens_hash_active",
            "token_hash",
            postgresql_where=text("is_used = false"),
        ),
        {"schema": "auth"},
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text("public.gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    action_type: Mapped[str] = mapped_column(
        Enum(
            "RESET_PASSWORD",
            "ACTIVATE_ACCOUNT",
            name="action_token_type_enum",
            schema="auth",
        ),
        nullable=False,
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    is_used: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="action_tokens")

    def is_valid(self) -> bool:
        """Cek apakah token masih valid (belum expired dan belum dipakai)"""
        import datetime as dt

        now = dt.datetime.now(dt.timezone.utc)
        expires = self.expires_at.replace(tzinfo=dt.timezone.utc) if self.expires_at.tzinfo is None else self.expires_at
        return not self.is_used and now < expires

    def mark_used(self) -> None:
        """Tandai token sebagai sudah digunakan"""
        self.is_used = True
