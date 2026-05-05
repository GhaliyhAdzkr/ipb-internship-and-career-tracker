import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app_backend.models.notification_queue import NotificationQueue
from app_backend.models.users import Users


def test_list_notifications(client, db_session, test_user, user_token):
    # Create notifications for current user
    notif_active = NotificationQueue(
        title="Aktif 1",
        message="Pesan 1",
        user_id=test_user.id,
        status="QUEUED",
        scheduled_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    notif_deleted = NotificationQueue(
        title="Deleted",
        message="Pesan",
        user_id=test_user.id,
        status="DELETED",
        scheduled_at=datetime.now(timezone.utc),
    )
    # Create notification for OTHER user
    other_user = Users(
        email="other@example.com",
        password_hash="hash",
        role="STUDENT",
        is_active=True,
    )
    db_session.add(other_user)
    db_session.commit()

    notif_other = NotificationQueue(
        title="Punya Orang",
        message="Pesan",
        user_id=other_user.id,
        status="QUEUED",
        scheduled_at=datetime.now(timezone.utc),
    )
    db_session.add_all([notif_active, notif_deleted, notif_other])
    db_session.commit()

    response = client.get(
        "/api/v1/notifications", headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Aktif 1"


def test_read_notification_authorization(client, db_session, test_user, user_token):
    other_user = Users(
        email="hacker@example.com",
        password_hash="hash",
        role="STUDENT",
        is_active=True,
    )
    db_session.add(other_user)
    db_session.commit()

    notif_other = NotificationQueue(
        title="Rahasia",
        message="Pesan rahasia",
        user_id=other_user.id,
        status="QUEUED",
    )
    db_session.add(notif_other)
    db_session.commit()

    # Attempt to read other's notification
    response = client.patch(
        f"/api/v1/notifications/{notif_other.id}/read",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    # In our implementation, if user doesn't own it, it returns 404
    assert response.status_code == 404
    assert "tidak ditemukan" in response.json()["detail"].lower()


def test_delete_notification(client, db_session, test_user, user_token):
    notif = NotificationQueue(
        title="Test Delete",
        message="Pesan",
        user_id=test_user.id,
        status="QUEUED",
    )
    db_session.add(notif)
    db_session.commit()

    # Get unread count before
    resp_count_before = client.get(
        "/api/v1/notifications/unread-count",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp_count_before.json()["unread_count"] == 1

    # Delete
    response = client.delete(
        f"/api/v1/notifications/{notif.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204

    # Verify db status is DELETED
    db_session.refresh(notif)
    assert notif.status == "DELETED"

    # Get unread count after
    resp_count_after = client.get(
        "/api/v1/notifications/unread-count",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp_count_after.json()["unread_count"] == 0
