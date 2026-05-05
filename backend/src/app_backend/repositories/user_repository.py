from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.users import Users
from app_backend.repositories.base import BaseRepository


class UserRepository(BaseRepository[Users]):
    def __init__(self, session: Session):
        super().__init__(Users, session)

    def get_by_email(self, email: str) -> Optional[Users]:
        query = select(Users).where(Users.email == email)
        return self.session.scalars(query).first()
