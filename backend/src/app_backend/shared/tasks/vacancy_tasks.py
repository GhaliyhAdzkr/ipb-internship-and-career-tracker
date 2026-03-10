"""
Vacancy Tasks – Background tasks untuk vacancy management.
Berjalan di queue terpisah untuk scraping dan auto-close.
"""

from datetime import datetime, timezone
from typing import Dict

from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_backend.models.base import Base
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
            results.append({
                "source_url": url,
                "status": "pending",
                "message": "Scraper not implemented",
            })

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
