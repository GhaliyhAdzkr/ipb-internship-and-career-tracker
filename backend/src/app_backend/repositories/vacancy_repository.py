from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app_backend.models.vacancies import Vacancies
from app_backend.repositories.base import BaseRepository


class VacancyRepository(BaseRepository[Vacancies]):
    def __init__(self, session: Session):
        super().__init__(Vacancies, session)

    def list_active(self, skip: int = 0, limit: int = 100) -> List[Vacancies]:
        query = select(Vacancies).options(joinedload(Vacancies.company)).where(Vacancies.is_active).offset(skip).limit(limit)
        return list(self.session.scalars(query).unique().all())

    def search(self, filters: list, skip: int = 0, limit: int = 100) -> List[Vacancies]:
        query = select(Vacancies).options(joinedload(Vacancies.company)).where(Vacancies.is_active, *filters).offset(skip).limit(limit)
        return list(self.session.scalars(query).unique().all())

    def count_active(self) -> int:
        query = select(func.count()).select_from(Vacancies).where(Vacancies.is_active)
        return self.session.execute(query).scalar_one()
