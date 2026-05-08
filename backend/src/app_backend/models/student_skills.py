"""
Model: public.student_skills
Relasi many-to-many antara student dan master_skills dengan level expertise.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.master_skills import MasterSkills
    from app_backend.models.profiles_student import ProfilesStudent


class StudentSkills(Base):
    __tablename__ = "student_skills"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 5", name="student_skills_level_check"),
        ForeignKeyConstraint(
            ["skill_id"],
            ["master_skills.id"],
            ondelete="CASCADE",
            name="student_skills_skill_id_fkey",
        ),
        ForeignKeyConstraint(
            ["student_id"],
            ["profiles_student.user_id"],
            ondelete="CASCADE",
            name="student_skills_student_id_fkey",
        ),
        Index("idx_skills_matching", "skill_id"),
    )

    student_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    level: Mapped[Optional[int]] = mapped_column(Integer)

    # Relationships
    skill: Mapped["MasterSkills"] = relationship("MasterSkills", back_populates="student_skills")
    student: Mapped["ProfilesStudent"] = relationship("ProfilesStudent", back_populates="student_skills")
