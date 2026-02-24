"""
Model: public.profiles_admin
Data profil fasilitator/admin (CDA IPB, dll).
"""

from __future__ import annotations

import datetime
import uuid
from typing import Optional

from sqlalchemy import (DateTime, ForeignKeyConstraint, String,
                        UniqueConstraint, Uuid, text)
from sqlalchemy.orm import Mapped, mapped_column

from app_backend.models.base import Base


class ProfilesAdmin(Base):
    __tablename__ = "profiles_admin"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
            ondelete="CASCADE",
            name="profiles_admin_user_id_fkey",
        ),
        UniqueConstraint("nip", name="profiles_admin_nip_key"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    unit_name: Mapped[str] = mapped_column(String(150), nullable=False)
    nip: Mapped[Optional[str]] = mapped_column(String(30))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
