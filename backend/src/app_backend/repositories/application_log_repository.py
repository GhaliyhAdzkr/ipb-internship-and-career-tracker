from sqlalchemy.orm import Session

from app_backend.models.application_logs import ApplicationLogs
from app_backend.repositories.base import BaseRepository


class ApplicationLogRepository(BaseRepository[ApplicationLogs]):
    def __init__(self, session: Session):
        super().__init__(ApplicationLogs, session)
