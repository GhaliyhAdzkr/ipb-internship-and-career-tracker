"""
Notification Tasks – Background tasks untuk notifikasi dan email.
Berjalan di queue terpisah untuk email sending dan cleanup.
"""

from datetime import datetime, timezone
from typing import Dict, List

from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_backend.models.auth_action_tokens import AuthActionTokens
from app_backend.models.notification_queue import NotificationQueue
from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.shared.database import get_database_url


@shared_task
def send_email_notification(
    notification_id: str,
    user_email: str,
    subject: str,
    message: str,
) -> Dict:
    """
    Task: Send email notification.
    Placeholder - implementasikan SMTP sending sesuai kebutuhan.
    """
    try:
        # Placeholder: Send email via SMTP
        # import smtplib, email
        # ...

        return {
            "status": "sent",
            "notification_id": notification_id,
            "recipient": user_email,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        return {
            "status": "failed",
            "error": str(exc),
        }


@shared_task
def process_notification_queue() -> Dict:
    """
    Task: Process queued notifications.
    Read from notification_queue dan send emails.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Get pending notifications
        pending_notifications = (
            session.query(NotificationQueue)
            .filter(NotificationQueue.status == "QUEUED")
            .limit(100)  # Process max 100 at a time
            .all()
        )

        processed = 0
        failed = 0

        for notif in pending_notifications:
            try:
                # Send email (placeholder)
                notif.status = "SENT"
                notif.sent_at = datetime.now(timezone.utc)
                processed += 1
            except Exception:
                notif.status = "FAILED"
                failed += 1

        session.commit()

        return {
            "status": "completed",
            "processed": processed,
            "failed": failed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        session.rollback()
        return {
            "status": "failed",
            "error": str(exc),
        }
    finally:
        session.close()


@shared_task
def cleanup_expired_tokens() -> Dict:
    """
    Task: Cleanup expired refresh tokens dan action tokens.
    Dijalankan secara terjadwal (cron) untuk maintenance.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        now = datetime.now(timezone.utc)

        # Cleanup expired refresh tokens
        expired_refresh = (
            session.query(UserRefreshTokens)
            .filter(
                UserRefreshTokens.is_revoked == False,
                UserRefreshTokens.expires_at < now,
            )
            .all()
        )
        refresh_deleted = len(expired_refresh)
        for token in expired_refresh:
            session.delete(token)

        # Cleanup expired action tokens
        expired_actions = (
            session.query(AuthActionTokens)
            .filter(AuthActionTokens.expires_at < now)
            .all()
        )
        action_deleted = len(expired_actions)
        for token in expired_actions:
            session.delete(token)

        session.commit()

        return {
            "status": "completed",
            "refresh_tokens_deleted": refresh_deleted,
            "action_tokens_deleted": action_deleted,
            "timestamp": now.isoformat(),
        }

    except Exception as exc:
        session.rollback()
        return {
            "status": "failed",
            "error": str(exc),
        }
    finally:
        session.close()


@shared_task
def send_bulk_notifications(user_ids: List[str], subject: str, message: str) -> Dict:
    """
    Task: Send bulk notifications ke multiple users.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        from app_backend.models.users import Users

        queued = 0
        for user_id in user_ids:
            user = session.query(Users).filter(Users.id == user_id).first()
            if user:
                notif = NotificationQueue(
                    user_id=user.id,
                    title=subject,
                    message=message,
                    status="QUEUED",
                    created_at=datetime.now(timezone.utc),
                )
                session.add(notif)
                queued += 1

        session.commit()

        return {
            "status": "completed",
            "queued": queued,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        session.rollback()
        return {
            "status": "failed",
            "error": str(exc),
        }
    finally:
        session.close()
