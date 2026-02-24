"""
Model: public.application_logs
Audit trail setiap perubahan status lamaran (termasuk bukti proof_url).
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKeyConstraint, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.applications import Applications
    from app_backend.models.users import Users


class ApplicationLogs(Base):
    __tablename__ = "application_logs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            ondelete="CASCADE",
            name="application_logs_application_id_fkey",
        ),
        ForeignKeyConstraint(
            ["changed_by"],
            ["auth.users.id"],
            ondelete="SET NULL",
            name="application_logs_changed_by_fkey",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("public.gen_random_uuid()")
    )
    application_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    new_status: Mapped[str] = mapped_column(
        Enum(
            "APPLIED",
            "SCREENING",
            "INTERVIEW",
            "OFFERED",
            "ACCEPTED",
            "REJECTED",
            "WITHDRAWN",
            name="app_status_enum",
        ),
        nullable=False,
    )
    previous_status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "APPLIED",
            "SCREENING",
            "INTERVIEW",
            "OFFERED",
            "ACCEPTED",
            "REJECTED",
            "WITHDRAWN",
            name="app_status_enum",
        )
    )
    changed_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    proof_url: Mapped[Optional[str]] = mapped_column(Text)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    application: Mapped["Applications"] = relationship(
        "Applications", back_populates="application_logs"
    )
    users: Mapped[Optional["Users"]] = relationship(
        "Users", back_populates="application_logs"
    )
