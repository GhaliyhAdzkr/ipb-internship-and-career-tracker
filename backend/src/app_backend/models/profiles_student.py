"""
Model: public.profiles_student
Data profil mahasiswa dengan relasi ke master_departments.
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
    ForeignKeyConstraint,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.applications import Applications
    from app_backend.models.document_requests import DocumentRequests
    from app_backend.models.master_departments import MasterDepartments
    from app_backend.models.placements import Placements
    from app_backend.models.student_skills import StudentSkills
    from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies


class ProfilesStudent(Base):
    __tablename__ = "profiles_student"
    __table_args__ = (
        CheckConstraint("semester > 0", name="profiles_student_semester_check"),
        ForeignKeyConstraint(
            ["department_id"],
            ["master_departments.id"],
            ondelete="RESTRICT",
            name="profiles_student_department_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
            ondelete="CASCADE",
            name="profiles_student_user_id_fkey",
        ),
        UniqueConstraint("nim", name="profiles_student_nim_key"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    nim: Mapped[str] = mapped_column(String(20), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    gpa: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text)
    cv_url: Mapped[Optional[str]] = mapped_column(Text)
    is_mbkm_eligible: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("true"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    department: Mapped[Optional["MasterDepartments"]] = relationship("MasterDepartments", back_populates="profiles_student")
    applications: Mapped[list["Applications"]] = relationship("Applications", back_populates="student")
    document_requests: Mapped[list["DocumentRequests"]] = relationship("DocumentRequests", back_populates="student")
    student_skills: Mapped[list["StudentSkills"]] = relationship("StudentSkills", back_populates="student")
    student_wishlist_vacancies: Mapped[list["StudentWishlistVacancies"]] = relationship(
        "StudentWishlistVacancies", back_populates="student"
    )
    placements: Mapped[list["Placements"]] = relationship("Placements", back_populates="student")
