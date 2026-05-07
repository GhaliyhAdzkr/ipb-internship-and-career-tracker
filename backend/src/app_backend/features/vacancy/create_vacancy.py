"""
Create Vacancy Feature – Command Handler.
Membuat lowongan baru dengan skills yang diperlukan.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills
from app_backend.schemas.vacancy import VacancyCreate, VacancyResponse


class CreateVacancyException(Exception):
    pass


@dataclass
class CreateVacancyCommand:
    payload: VacancyCreate
    created_by: Optional[uuid.UUID] = None


@dataclass
class CreateVacancyResult:
    vacancy: Optional[VacancyResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def create_vacancy_command_handler(
    command: CreateVacancyCommand,
    session: Session,
) -> CreateVacancyResult:
    """
    Business Rules:
    1. Company harus ada di master_external_companies.
    2. Tanggal close harus setelah tanggal open.
    3. Compensation range harus valid (min <= max).
    4. Skills yang dipilih harus ada di master_skills.
    """
    payload = command.payload

    # Validasi company exists
    company = session.get(MasterExternalCompanies, payload.company_id)
    if not company:
        return CreateVacancyResult(error_message="Perusahaan tidak ditemukan")

    # Validasi tanggal
    if payload.close_date <= payload.open_date:
        return CreateVacancyResult(error_message="Tanggal tutup harus setelah tanggal buka")

    # Validasi compensation range
    if payload.compensation_min and payload.compensation_max:
        if payload.compensation_min > payload.compensation_max:
            return CreateVacancyResult(error_message="Kompensasi minimum tidak boleh lebih besar dari maksimum")

    try:
        now = datetime.now(timezone.utc)

        # Create vacancy
        vacancy = Vacancies(
            id=uuid.uuid4(),
            company_id=payload.company_id,
            title=payload.title,
            description=payload.description,
            type=payload.type.value,
            open_date=payload.open_date,
            close_date=payload.close_date,
            location=payload.location,
            payment_type=(payload.payment_type.value if payload.payment_type else "UNPAID"),
            compensation_min=payload.compensation_min,
            compensation_max=payload.compensation_max,
            compensation_note=payload.compensation_note,
            source_url=str(payload.source_url) if payload.source_url else None,
            is_scraped=False,
            is_auto_close=True,
            is_active=True,
            created_by=command.created_by,
            created_at=now,
            updated_at=now,
        )

        session.add(vacancy)
        session.flush()

        # Add skills if provided
        if payload.skills:
            for skill_item in payload.skills:
                vacancy_skill = VacancySkills(
                    vacancy_id=vacancy.id,
                    skill_id=skill_item.skill_id,
                    is_mandatory=skill_item.is_mandatory,
                )
                session.add(vacancy_skill)

        session.commit()
        session.refresh(vacancy)

        return CreateVacancyResult(
            vacancy=VacancyResponse(
                id=vacancy.id,
                company_id=vacancy.company_id,
                title=vacancy.title,
                description=vacancy.description,
                type=vacancy.type,
                open_date=vacancy.open_date,
                close_date=vacancy.close_date,
                location=vacancy.location,
                payment_type=vacancy.payment_type,
                compensation_min=vacancy.compensation_min,
                compensation_max=vacancy.compensation_max,
                compensation_note=vacancy.compensation_note,
                source_url=vacancy.source_url,
                is_scraped=vacancy.is_scraped if vacancy.is_scraped else False,
                is_auto_close=vacancy.is_auto_close if vacancy.is_auto_close else True,
                is_active=vacancy.is_active if vacancy.is_active else True,
                created_at=vacancy.created_at,
                updated_at=vacancy.updated_at,
            )
        )

    except ValueError as exc:
        session.rollback()
        return CreateVacancyResult(error_message=str(exc))
    except Exception as exc:
        session.rollback()
        return CreateVacancyResult(error_message=f"Gagal membuat lowongan: {exc}")
