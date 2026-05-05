from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.profiles_admin import ProfilesAdmin
from app_backend.repositories.base import BaseRepository


class AdminRepository(BaseRepository[ProfilesAdmin]):
    def __init__(self, session: Session):
        super().__init__(ProfilesAdmin, session)

    def get_by_nip(self, nip: str) -> Optional[ProfilesAdmin]:
        query = select(ProfilesAdmin).where(ProfilesAdmin.nip == nip)
        return self.session.scalars(query).first()
