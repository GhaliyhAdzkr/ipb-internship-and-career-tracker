import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.student_skills import StudentSkills
    from app_backend.models.vacancy_skills import VacancySkills


class MasterSkills(Base):
    __tablename__ = "master_skills"
    __table_args__ = (UniqueConstraint("name", name="master_skills_name_key"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50))

    # Relationships
    student_skills: Mapped[list["StudentSkills"]] = relationship("StudentSkills", back_populates="skill")
    vacancy_skills: Mapped[list["VacancySkills"]] = relationship("VacancySkills", back_populates="skill")
