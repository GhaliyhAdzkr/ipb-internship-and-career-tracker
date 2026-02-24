"""
Model: public.vacancy_skills
Relasi many-to-many antara vacancies dan master_skills (prasyarat keahlian).
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKeyConstraint, Index, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.master_skills import MasterSkills
    from app_backend.models.vacancies import Vacancies


class VacancySkills(Base):
    __tablename__ = "vacancy_skills"
    __table_args__ = (
        ForeignKeyConstraint(
            ["skill_id"],
            ["master_skills.id"],
            ondelete="CASCADE",
            name="vacancy_skills_skill_id_fkey",
        ),
        ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancies.id"],
            ondelete="CASCADE",
            name="vacancy_skills_vacancy_id_fkey",
        ),
        Index("idx_vacancy_skills", "skill_id"),
    )

    vacancy_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    is_mandatory: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    # Relationships
    skill: Mapped["MasterSkills"] = relationship(
        "MasterSkills", back_populates="vacancy_skills"
    )
    vacancy: Mapped["Vacancies"] = relationship(
        "Vacancies", back_populates="vacancy_skills"
    )
