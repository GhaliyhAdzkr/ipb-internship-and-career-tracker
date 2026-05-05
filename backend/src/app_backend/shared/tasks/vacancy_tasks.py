"""
Vacancy Tasks – Background tasks untuk vacancy management.
Berjalan di queue terpisah untuk scraping dan auto-close.
"""

from datetime import datetime, timezone
from typing import Dict

from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_backend.models.vacancies import Vacancies
from app_backend.shared.database import get_database_url


@shared_task
def auto_close_expired_vacancies() -> Dict:
    """
    Task: Close vacancies yang sudah melampaui close_date.
    Dijalankan secara terjadwal (cron).
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        now = datetime.now(timezone.utc)

        # Find expired vacancies that are still active and have auto_close enabled
        expired_vacancies = (
            session.query(Vacancies)
            .filter(
                Vacancies.is_active == True,
                Vacancies.is_auto_close == True,
                Vacancies.close_date < now,
            )
            .all()
        )

        closed_count = 0
        for vacancy in expired_vacancies:
            vacancy.is_active = False
            vacancy.updated_at = now
            closed_count += 1

        session.commit()

        return {
            "status": "completed",
            "closed_count": closed_count,
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
def notify_expiring_wishlists() -> Dict:
    """
    Task: Notify students if a vacancy in their wishlist is closing in 3 days.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        from datetime import timedelta

        from app_backend.models.notification_queue import NotificationQueue
        from app_backend.models.student_wishlist_vacancies import \
            StudentWishlistVacancies

        now = datetime.now(timezone.utc)
        target_close_date_start = now + timedelta(days=2)
        target_close_date_end = now + timedelta(days=3)

        # Get vacancies closing in 3 days that are in wishlists
        expiring_wishlists = (
            session.query(StudentWishlistVacancies)
            .join(Vacancies)
            .filter(
                Vacancies.is_active == True,
                Vacancies.close_date >= target_close_date_start,
                Vacancies.close_date < target_close_date_end,
            )
            .all()
        )

        notified_count = 0
        for wishlist in expiring_wishlists:
            vacancy = wishlist.vacancy
            notif = NotificationQueue(
                title="Lowongan Wishlist Segera Tutup",
                message=f"Lowongan '{vacancy.title}' dari {vacancy.company.name} yang ada di wishlist Anda akan ditutup dalam 3 hari.",
                user_id=(
                    wishlist.student.user_id
                    if hasattr(wishlist, "student") and wishlist.student
                    else wishlist.student_id
                ),
                channel="ALL",
                status="QUEUED",
            )
            session.add(notif)
            notified_count += 1

        session.commit()

        return {
            "status": "completed",
            "notified_count": notified_count,
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
def scrape_vacancies(source_urls: list) -> Dict:
    """
    Task: Scrape vacancies dari portal eksternal.
    Untuk saat ini placeholder - implementasikan scraper sesuai kebutuhan.
    """
    try:
        results = []
        for url in source_urls:
            # Placeholder: Scrape vacancy dari URL
            # Extract: title, description, company, location, etc.
            results.append(
                {
                    "source_url": url,
                    "status": "pending",
                    "message": "Scraper not implemented",
                }
            )

        return {
            "status": "completed",
            "total": len(source_urls),
            "results": results,
        }

    except Exception as exc:
        return {
            "status": "failed",
            "error": str(exc),
        }


@shared_task
def cleanup_old_vacancies(days: int = 90) -> Dict:
    """
    Task: Hapus vacancies yang sudah tidak aktif dan terlalu lama.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        from datetime import timedelta

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        # Find old inactive vacancies
        old_vacancies = (
            session.query(Vacancies)
            .filter(
                Vacancies.is_active == False,
                Vacancies.updated_at < cutoff_date,
            )
            .all()
        )

        deleted_count = 0
        for vacancy in old_vacancies:
            session.delete(vacancy)
            deleted_count += 1

        session.commit()

        return {
            "status": "completed",
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat(),
        }

    except Exception as exc:
        session.rollback()
        return {
            "status": "failed",
            "error": str(exc),
        }
    finally:
        session.close()
