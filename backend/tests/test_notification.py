import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app_backend.models.notification_queue import NotificationQueue
from app_backend.models.users import Users


from unittest.mock import MagicMock, patch

from tests.conftest import STUDENT_USER_ID, NOW

NOTIF_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")


def test_list_notifications(client_as_student):
    with patch("app_backend.routers.api.notification.list_notifications_command_handler") as mock_handler:
        from app_backend.schemas.notification import NotificationResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            notifications=[
                NotificationResponse(
                    id=NOTIF_ID,
                    user_id=STUDENT_USER_ID,
                    title="Aktif 1",
                    message="Pesan 1",
                    status="QUEUED",
                    channel="ALL",
                    created_at=NOW,
                    scheduled_at=NOW,
                )
            ]
        )
        response = client_as_student.get("/api/v1/notifications")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Aktif 1"


def test_get_unread_count(client_as_student):
    with patch("app_backend.routers.api.notification.get_unread_count_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            count=5
        )
        response = client_as_student.get("/api/v1/notifications/unread-count")

    assert response.status_code == 200
    assert response.json()["unread_count"] == 5


def test_read_notification(client_as_student):
    with patch("app_backend.routers.api.notification.read_notification_command_handler") as mock_handler:
        from app_backend.schemas.notification import NotificationResponse

        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            notification=NotificationResponse(
                id=NOTIF_ID,
                user_id=STUDENT_USER_ID,
                title="Aktif 1",
                message="Pesan 1",
                status="SENT",
                channel="ALL",
                created_at=NOW,
                scheduled_at=NOW,
            )
        )
        response = client_as_student.patch(f"/api/v1/notifications/{NOTIF_ID}/read")

    assert response.status_code == 200
    assert response.json()["status"] == "SENT"


def test_read_notification_authorization(client_as_student):
    with patch("app_backend.routers.api.notification.read_notification_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: True,
            error_message="Notifikasi tidak ditemukan",
            error_code=404
        )
        response = client_as_student.patch(f"/api/v1/notifications/{NOTIF_ID}/read")

    assert response.status_code == 404
    assert "tidak ditemukan" in response.json()["detail"].lower()


def test_delete_notification(client_as_student):
    with patch("app_backend.routers.api.notification.delete_notification_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: False
        )
        response = client_as_student.delete(f"/api/v1/notifications/{NOTIF_ID}")

    assert response.status_code == 204
