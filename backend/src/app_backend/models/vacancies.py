"""
Model: public.vacancies
Lowongan magang/kerja yang dikurasi atau discraped dari portal publik.
"""

from __future__ import annotations

import datetime
import decimal
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Index,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.applications import Applications
    from app_backend.models.document_requests import DocumentRequests
    from app_backend.models.master_external_companies import MasterExternalCompanies
    from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies
    from app_backend.models.users import Users
    from app_backend.models.vacancy_skills import VacancySkills


class Vacancies(Base):
    __tablename__ = "vacancies"
    __table_args__ = (
        CheckConstraint("close_date >= open_date", name="vacancies_check"),
        CheckConstraint(
            "compensation_min >= 0::numeric",
            name="vacancies_compensation_nominal_check",
        ),
        CheckConstraint(
            "compensation_min >= 0::numeric AND (compensation_max IS NULL OR compensation_max >= compensation_min)",
            name="check_compensation_range",
        ),
        ForeignKeyConstraint(
            ["company_id"],
            ["master_external_companies.id"],
            ondelete="RESTRICT",
            name="vacancies_company_id_fkey",
        ),
        ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            ondelete="SET NULL",
            name="vacancies_created_by_fkey",
        ),
        PrimaryKeyConstraint("id", name="vacancies_pkey"),
        Index("idx_vacancies_active", "open_date", "close_date"),
        Index("idx_vacancies_search_vector", "search_vector", postgresql_using="gin"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    search_vector: Mapped[Optional[any]] = mapped_column(TSVECTOR, nullable=True)
    type: Mapped[str] = mapped_column(
        Enum(
            "INTERNSHIP_GENERAL",
            "MBKM_INTERNSHIP",
            "MBKM_STUDY_INDEPENDENT",
            "FULL_TIME",
            name="vacancy_type_enum",
        ),
        nullable=False,
    )
    open_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    close_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    location: Mapped[Optional[str]] = mapped_column(String(150))
    payment_type: Mapped[Optional[str]] = mapped_column(
        Enum("PAID", "UNPAID", "ALLOWANCE_ONLY", name="payment_type_enum"),
        server_default=text("'UNPAID'::payment_type_enum"),
    )
    compensation_min: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    compensation_max: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    compensation_note: Mapped[Optional[str]] = mapped_column(Text)
    source_url: Mapped[Optional[str]] = mapped_column(Text)
    is_scraped: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    is_auto_close: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("true"))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("true"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    company: Mapped["MasterExternalCompanies"] = relationship("MasterExternalCompanies", back_populates="vacancies")
    users: Mapped[Optional["Users"]] = relationship("Users", back_populates="vacancies")
    applications: Mapped[list["Applications"]] = relationship("Applications", back_populates="vacancy")
    document_requests: Mapped[list["DocumentRequests"]] = relationship("DocumentRequests", back_populates="reference_vacancy")
    student_wishlist_vacancies: Mapped[list["StudentWishlistVacancies"]] = relationship(
        "StudentWishlistVacancies", back_populates="vacancy"
    )
    vacancy_skills: Mapped[list["VacancySkills"]] = relationship("VacancySkills", back_populates="vacancy")
