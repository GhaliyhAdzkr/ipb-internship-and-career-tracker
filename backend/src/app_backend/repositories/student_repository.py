from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.profiles_student import ProfilesStudent
from app_backend.repositories.base import BaseRepository


class StudentRepository(BaseRepository[ProfilesStudent]):
    def __init__(self, session: Session):
        super().__init__(ProfilesStudent, session)

    def get_by_nim(self, nim: str) -> Optional[ProfilesStudent]:
        query = select(ProfilesStudent).where(ProfilesStudent.nim == nim)
        return self.session.scalars(query).first()
