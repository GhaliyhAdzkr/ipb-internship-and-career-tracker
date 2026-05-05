from sqlalchemy.orm import Session

from app_backend.models.activity_logs import ActivityLogs
from app_backend.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLogs]):
    def __init__(self, session: Session):
        super().__init__(ActivityLogs, session)
