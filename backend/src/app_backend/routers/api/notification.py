import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app_backend.domain.user import User as DomainUser
from app_backend.features.notification.delete_notification import (
    DeleteNotificationCommand, delete_notification_command_handler)
from app_backend.features.notification.get_unread_count import (
    GetUnreadCountCommand, get_unread_count_command_handler)
from app_backend.features.notification.list_notifications import (
    ListNotificationsCommand, list_notifications_command_handler)
from app_backend.features.notification.read_notification import (
    ReadNotificationCommand, read_notification_command_handler)
from app_backend.schemas.notification import NotificationResponse
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import require_authenticated_user

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.get(
    "",
    response_model=List[NotificationResponse],
    summary="Daftar notifikasi aktif untuk user yang sedang login",
)
def list_notifications(
    current_user: DomainUser = Depends(require_authenticated_user),
    session: Session = Depends(get_session),
):
    result = list_notifications_command_handler(
        command=ListNotificationsCommand(user_id=current_user.id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error_message
        )
    return result.notifications


@router.get(
    "/unread-count",
    summary="Return jumlah notifikasi belum dibaca",
)
def get_unread_count(
    current_user: DomainUser = Depends(require_authenticated_user),
    session: Session = Depends(get_session),
):
    result = get_unread_count_command_handler(
        command=GetUnreadCountCommand(user_id=current_user.id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error_message
        )
    return {"unread_count": result.count}


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Tandai notifikasi sebagai sudah dibaca",
)
def read_notification(
    notification_id: uuid.UUID,
    current_user: DomainUser = Depends(require_authenticated_user),
    session: Session = Depends(get_session),
):
    result = read_notification_command_handler(
        command=ReadNotificationCommand(
            notification_id=notification_id, user_id=current_user.id
        ),
        session=session,
    )
    if result.got_error():
        err_status = (
            status.HTTP_400_BAD_REQUEST
            if result.error_code == 400
            else result.error_code
        )
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return result.notification


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete notifikasi dari inbox",
)
def delete_notification(
    notification_id: uuid.UUID,
    current_user: DomainUser = Depends(require_authenticated_user),
    session: Session = Depends(get_session),
):
    result = delete_notification_command_handler(
        command=DeleteNotificationCommand(
            notification_id=notification_id, user_id=current_user.id
        ),
        session=session,
    )
    if result.got_error():
        err_status = (
            status.HTTP_400_BAD_REQUEST
            if result.error_code == 400
            else result.error_code
        )
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return
