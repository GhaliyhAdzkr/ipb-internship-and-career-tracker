import html
import json
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests
from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.models.master_skills import MasterSkills
from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills
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
                Vacancies.is_active,
                Vacancies.is_auto_close,
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
        from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies

        now = datetime.now(timezone.utc)
        target_close_date_start = now + timedelta(days=2)
        target_close_date_end = now + timedelta(days=3)

        # Get vacancies closing in 3 days that are in wishlists
        expiring_wishlists = (
            session.query(StudentWishlistVacancies)
            .join(Vacancies)
            .filter(
                Vacancies.is_active,
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
                user_id=(wishlist.student.user_id if hasattr(wishlist, "student") and wishlist.student else wishlist.student_id),
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


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = html.unescape(str(value))
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _meta_content(html_text: str, key: str) -> str:
    patterns = [
        rf'<meta[^>]+property=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+name=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']{re.escape(key)}["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return _clean_text(match.group(1))
    return ""


def _first_match(html_text: str, pattern: str) -> str:
    match = re.search(pattern, html_text, flags=re.IGNORECASE | re.DOTALL)
    return _clean_text(match.group(1)) if match else ""


def _parse_datetime(value: Any) -> Optional[datetime]:
    if not value:
        return None
    raw = str(value).strip()
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(raw[:10], "%Y-%m-%d")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _iter_jsonld_nodes(value: Any):
    if isinstance(value, list):
        for item in value:
            yield from _iter_jsonld_nodes(item)
    elif isinstance(value, dict):
        yield value
        graph = value.get("@graph")
        if graph:
            yield from _iter_jsonld_nodes(graph)


def _find_jobposting(html_text: str) -> Optional[dict]:
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for script in scripts:
        try:
            data = json.loads(html.unescape(script.strip()))
        except json.JSONDecodeError:
            continue
        for node in _iter_jsonld_nodes(data):
            node_type = node.get("@type")
            types = node_type if isinstance(node_type, list) else [node_type]
            if any(str(item).lower() == "jobposting" for item in types if item):
                return node
    return None


def _nested_text(value: Any, *keys: str) -> str:
    current = value
    for key in keys:
        if isinstance(current, list):
            current = current[0] if current else {}
        if not isinstance(current, dict):
            return ""
        current = current.get(key)
    if isinstance(current, dict):
        return ""
    if isinstance(current, list):
        return _clean_text(", ".join(str(item) for item in current))
    return _clean_text(current)


def _parse_salary(value: Any) -> tuple[Optional[Decimal], Optional[Decimal], Optional[str]]:
    if not value:
        return None, None, None
    salary_value = value
    if isinstance(value, dict):
        salary_value = value.get("value", value)
    if not isinstance(salary_value, dict):
        try:
            amount = Decimal(str(salary_value))
            return amount, None, None
        except (InvalidOperation, TypeError):
            return None, None, _clean_text(salary_value)

    min_value = salary_value.get("minValue") or salary_value.get("value")
    max_value = salary_value.get("maxValue")
    unit = salary_value.get("unitText")

    def to_decimal(raw: Any) -> Optional[Decimal]:
        try:
            return Decimal(str(raw)) if raw not in (None, "") else None
        except (InvalidOperation, TypeError):
            return None

    return to_decimal(min_value), to_decimal(max_value), _clean_text(unit)


def _company_from_url(source_url: str) -> str:
    host = urlparse(source_url).hostname or "Perusahaan Eksternal"
    parts = host.replace("www.", "").split(".")
    return parts[0].replace("-", " ").title() if parts else "Perusahaan Eksternal"


def _parse_vacancy_page(source_url: str, html_text: str, default_close_days: int = 30) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    job = _find_jobposting(html_text) or {}

    title = _clean_text(job.get("title")) or _meta_content(html_text, "og:title") or _first_match(html_text, r"<h1[^>]*>(.*?)</h1>")
    description = _clean_text(job.get("description")) or _meta_content(html_text, "description")
    if not description:
        description = _clean_text(html_text)[:2000]

    company = job.get("hiringOrganization") or {}
    company_name = _nested_text(company, "name") or _company_from_url(source_url)
    company_url = _nested_text(company, "sameAs") or _nested_text(company, "url")
    logo_url = _nested_text(company, "logo")

    location = _nested_text(job, "jobLocation", "address", "addressLocality")
    region = _nested_text(job, "jobLocation", "address", "addressRegion")
    country = _nested_text(job, "jobLocation", "address", "addressCountry")
    location = ", ".join(part for part in [location, region, country] if part) or _meta_content(html_text, "job-location")

    open_date = _parse_datetime(job.get("datePosted")) or now
    close_date = _parse_datetime(job.get("validThrough")) or (now + timedelta(days=default_close_days))
    if close_date < open_date:
        close_date = open_date + timedelta(days=default_close_days)

    employment_type = _clean_text(job.get("employmentType")).upper()
    vacancy_type = "FULL_TIME" if "FULL_TIME" in employment_type else "INTERNSHIP_GENERAL"
    salary_min, salary_max, salary_note = _parse_salary(job.get("baseSalary"))
    payment_type = "PAID" if salary_min or salary_max else "UNPAID"

    return {
        "title": title[:200] or "Lowongan dari Portal Eksternal",
        "description": description if len(description) >= 20 else f"{description} Detail lowongan tersedia pada sumber asli.",
        "company_name": company_name[:150],
        "company_website_url": company_url or f"{urlparse(source_url).scheme}://{urlparse(source_url).netloc}",
        "company_logo_url": logo_url or None,
        "industry": _clean_text(job.get("industry"))[:100] or None,
        "type": vacancy_type,
        "open_date": open_date,
        "close_date": close_date,
        "location": location[:150] or None,
        "payment_type": payment_type,
        "compensation_min": salary_min,
        "compensation_max": salary_max,
        "compensation_note": salary_note,
        "source_url": source_url,
    }


def _get_or_create_company(session, parsed: Dict[str, Any]) -> MasterExternalCompanies:
    company_name = parsed["company_name"]
    company = (
        session.query(MasterExternalCompanies)
        .filter(func.lower(MasterExternalCompanies.name) == company_name.lower())
        .first()
    )
    if company:
        if not company.website_url and parsed.get("company_website_url"):
            company.website_url = parsed["company_website_url"]
        if not company.logo_url and parsed.get("company_logo_url"):
            company.logo_url = parsed["company_logo_url"]
        if not company.industry and parsed.get("industry"):
            company.industry = parsed["industry"]
        return company

    company = MasterExternalCompanies(
        name=company_name,
        industry=parsed.get("industry"),
        website_url=parsed.get("company_website_url"),
        logo_url=parsed.get("company_logo_url"),
        created_at=datetime.now(timezone.utc),
    )
    session.add(company)
    session.flush()
    return company


def _attach_matching_skills(session, vacancy: Vacancies, parsed: Dict[str, Any]) -> int:
    searchable = f"{parsed.get('title', '')} {parsed.get('description', '')}".lower()
    skills = session.query(MasterSkills).all()
    matched_count = 0
    for skill in skills:
        name = (skill.name or "").strip()
        if name and re.search(rf"\b{re.escape(name.lower())}\b", searchable):
            session.add(VacancySkills(vacancy_id=vacancy.id, skill_id=skill.id, is_mandatory=True))
            matched_count += 1
    return matched_count


@shared_task
def scrape_vacancies(source_urls: list, default_close_days: int = 30) -> Dict:
    """
    Scrape lowongan dari URL eksternal, normalisasi ke schema Vacancies,
    lalu simpan sebagai hasil scraping untuk dikurasi admin.
    """
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    session = Session()
    results = []

    try:
        for raw_url in source_urls:
            source_url = str(raw_url).strip()
            try:
                existing = session.query(Vacancies).filter(Vacancies.source_url == source_url).first()
                if existing:
                    results.append(
                        {
                            "source_url": source_url,
                            "status": "skipped",
                            "message": "Lowongan dari URL ini sudah ada.",
                            "vacancy_id": str(existing.id),
                            "title": existing.title,
                        }
                    )
                    continue

                response = requests.get(
                    source_url,
                    headers={
                        "User-Agent": "IPB-Career-Tracker/1.0 (+https://ipb.ac.id)",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    },
                    timeout=20,
                )
                response.raise_for_status()

                parsed = _parse_vacancy_page(source_url, response.text, default_close_days=default_close_days)
                company = _get_or_create_company(session, parsed)
                vacancy = Vacancies(
                    company_id=company.id,
                    title=parsed["title"],
                    description=parsed["description"],
                    type=parsed["type"],
                    open_date=parsed["open_date"],
                    close_date=parsed["close_date"],
                    location=parsed["location"],
                    payment_type=parsed["payment_type"],
                    compensation_min=parsed["compensation_min"],
                    compensation_max=parsed["compensation_max"],
                    compensation_note=parsed["compensation_note"],
                    source_url=source_url,
                    is_scraped=True,
                    is_auto_close=True,
                    is_active=False,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(vacancy)
                session.flush()
                matched_skills = _attach_matching_skills(session, vacancy, parsed)
                session.commit()
                results.append(
                        {
                            "source_url": source_url,
                            "status": "imported",
                            "message": f"Lowongan berhasil diimpor sebagai hasil scraping pending kurasi. {matched_skills} skill cocok otomatis.",
                            "vacancy_id": str(vacancy.id),
                            "title": vacancy.title,
                        }
                )
            except Exception as exc:
                session.rollback()
                results.append(
                    {
                        "source_url": source_url,
                        "status": "failed",
                        "message": str(exc),
                    }
                )

        imported_count = sum(1 for item in results if item["status"] == "imported")
        skipped_count = sum(1 for item in results if item["status"] == "skipped")
        failed_count = sum(1 for item in results if item["status"] == "failed")
        return {
            "status": "completed" if failed_count == 0 else "partial",
            "total": len(source_urls),
            "imported_count": imported_count,
            "skipped_count": skipped_count,
            "failed_count": failed_count,
            "results": results,
        }

    except Exception as exc:
        session.rollback()
        return {
            "status": "failed",
            "total": len(source_urls),
            "imported_count": 0,
            "skipped_count": 0,
            "failed_count": len(source_urls),
            "results": results,
            "error": str(exc),
        }
    finally:
        session.close()


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
                not Vacancies.is_active,
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
