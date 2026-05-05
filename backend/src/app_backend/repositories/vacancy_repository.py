from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.vacancies import Vacancies
from app_backend.repositories.base import BaseRepository


class VacancyRepository(BaseRepository[Vacancies]):
    def __init__(self, session: Session):
        super().__init__(Vacancies, session)

    def list_active(self, skip: int = 0, limit: int = 100) -> List[Vacancies]:
        query = (
            select(Vacancies)
            .where(Vacancies.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.scalars(query).all())

    def search(self, filters: list, skip: int = 0, limit: int = 100) -> List[Vacancies]:
        query = (
            select(Vacancies)
            .where(Vacancies.is_active == True, *filters)
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.scalars(query).all())
