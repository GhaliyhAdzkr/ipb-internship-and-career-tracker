import uuid
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy.orm import Session

from app_backend.models.notification_queue import NotificationQueue


@dataclass
class ListNotificationsCommand:
    user_id: uuid.UUID


@dataclass
class ListNotificationsResult:
    notifications: Optional[List[NotificationQueue]] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_notifications_command_handler(
    command: ListNotificationsCommand,
    session: Session,
) -> ListNotificationsResult:
    notifications = (
        session.query(NotificationQueue)
        .filter(
            NotificationQueue.user_id == command.user_id,
            NotificationQueue.status != "DELETED",
        )
        .order_by(NotificationQueue.scheduled_at.desc())
        .all()
    )

    return ListNotificationsResult(notifications=notifications)
