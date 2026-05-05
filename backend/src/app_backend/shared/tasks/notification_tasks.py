"""
Notification Tasks – Background tasks untuk notifikasi dan email.
Berjalan di queue terpisah untuk email sending dan cleanup.
"""

import email.message
import smtplib
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_backend.conf.settings import settings
from app_backend.models.auth_action_tokens import AuthActionTokens
from app_backend.models.notification_queue import NotificationQueue
from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.shared.database import get_database_url


@shared_task
def send_email_notification(
    notification_id: str,
) -> Dict:
    """
    Task: Send email notification via SMTP (e.g. Resend).
    Queries the notification, sends the email, and updates the status to SENT.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        from sqlalchemy.orm import joinedload
        notif = session.query(NotificationQueue).options(joinedload(NotificationQueue.user)).filter_by(id=notification_id).first()
        if not notif or notif.status != "PROCESSING":
            return {"status": "skipped", "reason": "Not found or not processing"}
            
        user_email = notif.user.email if notif.user else None
        subject = notif.title
        message = notif.message
        
        if not user_email:
            notif.status = "FAILED"
            session.commit()
            return {"status": "failed", "error": "No email address"}

        msg = email.message.EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
        msg["To"] = user_email
        
        # Build minimal HTML email template
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #0c2340; color: #fff; padding: 15px; text-align: center; border-radius: 5px 5px 0 0; }}
                    .content {{ padding: 20px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 5px 5px; }}
                    .footer {{ margin-top: 20px; font-size: 0.8em; color: #777; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>IPB Internship & Career Tracker</h2>
                    </div>
                    <div class="content">
                        <p>Halo,</p>
                        <p>{message}</p>
                    </div>
                    <div class="footer">
                        <p>Notifikasi ini dikirim secara otomatis oleh sistem. Mohon tidak membalas email ini.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        msg.set_content(message)
        msg.add_alternative(html_content, subtype='html')

        # Connect and send
        if settings.smtp_port == 465:
            server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
        else:
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
            server.starttls()
            
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        
        notif.status = "SENT"
        notif.sent_at = datetime.now(timezone.utc)
        session.commit()

        return {
            "status": "sent",
            "notification_id": notification_id,
            "recipient": user_email,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        if 'notif' in locals() and notif:
            notif.status = "FAILED"
            session.commit()
        return {
            "status": "failed",
            "error": str(exc),
        }
    finally:
        session.close()


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
        # Get pending notifications with Row Lock (SKIP LOCKED) to prevent concurrent processing
        pending_notifications = (
            session.query(NotificationQueue)
            .filter(
                NotificationQueue.status == "QUEUED",
                NotificationQueue.scheduled_at <= datetime.now(timezone.utc)
            )
            .limit(100)  # Process max 100 at a time
            .with_for_update(skip_locked=True)
            .all()
        )

        processed = 0

        # Mark as processing first
        notif_ids = []
        for notif in pending_notifications:
            notif.status = "PROCESSING"
            notif_ids.append(str(notif.id))
            processed += 1

        session.commit()
        
        # Dispatch to async child tasks
        for nid in notif_ids:
            send_email_notification.delay(notification_id=nid)

        return {
            "status": "completed",
            "dispatched": processed,
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
        thirty_days_ago = now - timedelta(days=30)

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

        # Cleanup old notifications
        old_notifications = (
            session.query(NotificationQueue)
            .filter(
                NotificationQueue.created_at < thirty_days_ago,
                NotificationQueue.status.in_(["SENT", "DELETED"])
            )
            .all()
        )
        notif_deleted = len(old_notifications)
        for notif in old_notifications:
            session.delete(notif)

        session.commit()

        return {
            "status": "completed",
            "refresh_tokens_deleted": refresh_deleted,
            "action_tokens_deleted": action_deleted,
            "notifications_deleted": notif_deleted,
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
