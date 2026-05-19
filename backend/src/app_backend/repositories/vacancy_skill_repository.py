from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.vacancy_skills import VacancySkills
from app_backend.repositories.base import BaseRepository


class VacancySkillRepository(BaseRepository[VacancySkills]):
    def __init__(self, session: Session):
        super().__init__(VacancySkills, session)

    def get_by_vacancy_id(self, vacancy_id) -> List[VacancySkills]:
        query = select(VacancySkills).where(VacancySkills.vacancy_id == vacancy_id)
        return list(self.session.scalars(query).all())
