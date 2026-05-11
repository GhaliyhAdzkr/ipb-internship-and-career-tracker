"""
Model: public.master_external_companies
Katalog perusahaan eksternal untuk referensi lowongan.
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Index, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.placements import Placements
    from app_backend.models.vacancies import Vacancies


class MasterExternalCompanies(Base):
    __tablename__ = "master_external_companies"
    __table_args__ = (
        UniqueConstraint("name", name="master_external_companies_name_key"),
        Index("idx_master_companies_name", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    website_url: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    vacancies: Mapped[list["Vacancies"]] = relationship("Vacancies", back_populates="company")
    placements: Mapped[list["Placements"]] = relationship("Placements", back_populates="company")
