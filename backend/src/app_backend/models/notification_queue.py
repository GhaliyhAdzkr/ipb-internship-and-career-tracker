"""
Model: public.notification_queue
Antrian notifikasi in-app dan email.
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (DateTime, ForeignKeyConstraint, Index, String, Text,
                        Uuid, text)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.users import Users


class NotificationQueue(Base):
    __tablename__ = "notification_queue"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
            ondelete="CASCADE",
            name="notification_queue_user_id_fkey",
        ),
        Index("idx_notif_pending", "scheduled_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("public.gen_random_uuid()")
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    channel: Mapped[Optional[str]] = mapped_column(
        String(20), server_default=text("'ALL'::character varying")
    )
    scheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True), server_default=text("CURRENT_TIMESTAMP")
    )
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    status: Mapped[Optional[str]] = mapped_column(
        String(20), server_default=text("'QUEUED'::character varying")
    )

    # Relationships
    user: Mapped[Optional["Users"]] = relationship(
        "Users", back_populates="notification_queue"
    )
