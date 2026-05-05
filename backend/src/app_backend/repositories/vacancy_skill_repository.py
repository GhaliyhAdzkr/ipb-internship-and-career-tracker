from sqlalchemy.orm import Session

from app_backend.models.vacancy_skills import VacancySkills
from app_backend.repositories.base import BaseRepository


class VacancySkillRepository(BaseRepository[VacancySkills]):
    def __init__(self, session: Session):
        super().__init__(VacancySkills, session)
