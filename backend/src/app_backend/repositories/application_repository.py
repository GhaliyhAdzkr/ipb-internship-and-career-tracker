from sqlalchemy.orm import Session

from app_backend.models.applications import Applications
from app_backend.repositories.base import BaseRepository


class ApplicationRepository(BaseRepository[Applications]):
    def __init__(self, session: Session):
        super().__init__(Applications, session)
