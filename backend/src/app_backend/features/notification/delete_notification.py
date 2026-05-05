import uuid
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.notification_queue import NotificationQueue


@dataclass
class DeleteNotificationCommand:
    notification_id: uuid.UUID
    user_id: uuid.UUID


@dataclass
class DeleteNotificationResult:
    error_message: Optional[str] = None
    error_code: HTTPStatus = HTTPStatus.BAD_REQUEST

    def got_error(self) -> bool:
        return self.error_message is not None


def delete_notification_command_handler(
    command: DeleteNotificationCommand,
    session: Session,
) -> DeleteNotificationResult:
    notification = (
        session.query(NotificationQueue)
        .filter(
            NotificationQueue.id == command.notification_id,
            NotificationQueue.user_id == command.user_id,
        )
        .first()
    )

    if not notification:
        return DeleteNotificationResult(
            error_message="Notifikasi tidak ditemukan", error_code=HTTPStatus.NOT_FOUND
        )

    # Soft delete
    notification.status = "DELETED"
    session.commit()

    return DeleteNotificationResult()
