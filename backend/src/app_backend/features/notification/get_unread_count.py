import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.notification_queue import NotificationQueue


@dataclass
class GetUnreadCountCommand:
    user_id: uuid.UUID


@dataclass
class GetUnreadCountResult:
    count: int = 0
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def get_unread_count_command_handler(
    command: GetUnreadCountCommand,
    session: Session,
) -> GetUnreadCountResult:
    count = (
        session.query(NotificationQueue)
        .filter(
            NotificationQueue.user_id == command.user_id,
            NotificationQueue.status.in_(["QUEUED", "SENT"]),  # not READ or DELETED
        )
        .count()
    )

    return GetUnreadCountResult(count=count)
