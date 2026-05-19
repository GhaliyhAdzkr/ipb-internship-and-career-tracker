from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills
from app_backend.schemas.vacancy import VacancyResponse, VacancyUpdate


class UpdateVacancyException(Exception):
    pass


@dataclass
class UpdateVacancyCommand:
    vacancy_id: uuid.UUID
    payload: VacancyUpdate


@dataclass
class UpdateVacancyResult:
    vacancy: Optional[VacancyResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def update_vacancy_command_handler(
    command: UpdateVacancyCommand,
    session: Session,
) -> UpdateVacancyResult:
    """
    Business Rules:
    1. Vacancy harus ada.
    2. Validasi tanggal jika diupdate.
    3. Validasi compensation range jika diupdate.
    4. Skills bisa diupdate (replace all).
    """
    payload = command.payload
    vacancy = session.get(Vacancies, command.vacancy_id)

    if not vacancy:
        return UpdateVacancyResult(error_message="Lowongan tidak ditemukan")

    # Validasi tanggal jika diupdate
    open_date = payload.open_date or vacancy.open_date
    close_date = payload.close_date or vacancy.close_date

    if close_date <= open_date:
        return UpdateVacancyResult(error_message="Tanggal tutup harus setelah tanggal buka")

    # Validasi compensation range
    comp_min = payload.compensation_min or vacancy.compensation_min
    comp_max = payload.compensation_max or vacancy.compensation_max

    if comp_min and comp_max and comp_min > comp_max:
        return UpdateVacancyResult(error_message="Kompensasi minimum tidak boleh lebih besar dari maksimum")

    try:
        now = datetime.now(timezone.utc)

        # Update basic fields
        if payload.title is not None:
            vacancy.title = payload.title
        if payload.company_id is not None:
            vacancy.company_id = payload.company_id
        if payload.description is not None:
            vacancy.description = payload.description
        if payload.type is not None:
            vacancy.type = payload.type.value
        if payload.open_date is not None:
            vacancy.open_date = payload.open_date
        if payload.close_date is not None:
            vacancy.close_date = payload.close_date
        if payload.location is not None:
            vacancy.location = payload.location
        if payload.payment_type is not None:
            vacancy.payment_type = payload.payment_type.value
        if payload.compensation_min is not None:
            vacancy.compensation_min = payload.compensation_min
        if payload.compensation_max is not None:
            vacancy.compensation_max = payload.compensation_max
        if payload.compensation_note is not None:
            vacancy.compensation_note = payload.compensation_note
        if payload.source_url is not None:
            vacancy.source_url = str(payload.source_url)
        if payload.is_active is not None:
            vacancy.is_active = payload.is_active
        if payload.is_auto_close is not None:
            vacancy.is_auto_close = payload.is_auto_close

        vacancy.updated_at = now

        # Update skills if provided
        if payload.skills is not None:
            # Delete existing skills
            session.query(VacancySkills).filter(VacancySkills.vacancy_id == vacancy.id).delete()

            # Add new skills
            for skill_item in payload.skills:
                vacancy_skill = VacancySkills(
                    vacancy_id=vacancy.id,
                    skill_id=skill_item.skill_id,
                    is_mandatory=(skill_item.is_mandatory if skill_item.is_mandatory is not None else True),
                )
                session.add(vacancy_skill)

        session.commit()
        session.refresh(vacancy)

        return UpdateVacancyResult(
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
        return UpdateVacancyResult(error_message=str(exc))
    except Exception as exc:
        session.rollback()
        return UpdateVacancyResult(error_message=f"Gagal mengupdate lowongan: {exc}")
