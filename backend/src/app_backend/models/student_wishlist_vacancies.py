"""
Model: public.student_wishlist_vacancies
Lowongan yang di-bookmark oleh mahasiswa beserta catatan pribadi.
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.profiles_student import ProfilesStudent
    from app_backend.models.vacancies import Vacancies


class StudentWishlistVacancies(Base):
    __tablename__ = "student_wishlist_vacancies"
    __table_args__ = (
        ForeignKeyConstraint(
            ["student_id"],
            ["profiles_student.user_id"],
            ondelete="CASCADE",
            name="student_wishlist_vacancies_student_id_fkey",
        ),
        ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancies.id"],
            ondelete="CASCADE",
            name="student_wishlist_vacancies_vacancy_id_fkey",
        ),
        UniqueConstraint(
            "student_id",
            "vacancy_id",
            name="student_wishlist_vacancies_student_id_vacancy_id_key",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column("note", Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    student: Mapped["ProfilesStudent"] = relationship("ProfilesStudent", back_populates="student_wishlist_vacancies")
    vacancy: Mapped["Vacancies"] = relationship("Vacancies", back_populates="student_wishlist_vacancies")
