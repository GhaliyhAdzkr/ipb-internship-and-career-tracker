"""
Model: public.activity_logs
Logbook harian aktivitas magang (raw dan yang sudah di-enhance AI).
"""

from __future__ import annotations

import datetime
import decimal
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKeyConstraint, Index, Numeric, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.placements import Placements


class ActivityLogs(Base):
    __tablename__ = "activity_logs"
    __table_args__ = (
        CheckConstraint(
            "duration_hours > 0::numeric AND duration_hours <= 24::numeric",
            name="activity_logs_duration_hours_check",
        ),
        ForeignKeyConstraint(
            ["placement_id"],
            ["placements.id"],
            ondelete="CASCADE",
            name="activity_logs_placement_id_fkey",
        ),
        Index("idx_activity_logs_date", "placement_id", "activity_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text("public.gen_random_uuid()"))
    placement_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    activity_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    duration_hours: Mapped[decimal.Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    description_raw: Mapped[str] = mapped_column(Text, nullable=False)
    description_ai_enhanced: Mapped[Optional[str]] = mapped_column(Text)
    attachment_url: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    placement: Mapped["Placements"] = relationship("Placements", back_populates="activity_logs")
