from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills
from app_backend.schemas.vacancy import CompanyInfo, SkillRequirement, VacancyDetailResponse


class GetVacancyException(Exception):
    pass


@dataclass
class GetVacancyCommand:
    vacancy_id: uuid.UUID
    include_skills: bool = True


@dataclass
class GetVacancyResult:
    vacancy: Optional[VacancyDetailResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def get_vacancy_command_handler(
    command: GetVacancyCommand,
    session: Session,
) -> GetVacancyResult:
    """
    Ambil detail vacancy dengan company info dan skills.
    """
    vacancy = session.query(Vacancies).options(joinedload(Vacancies.company)).filter(Vacancies.id == command.vacancy_id).first()

    if not vacancy:
        return GetVacancyResult(error_message="Lowongan tidak ditemukan")

    # Get skills if requested
    skills = []
    if command.include_skills:
        vacancy_skills = (
            session.query(VacancySkills)
            .options(joinedload(VacancySkills.skill))
            .filter(VacancySkills.vacancy_id == vacancy.id)
            .all()
        )
        skills = [
            SkillRequirement(
                skill_id=vs.skill_id,
                skill_name=vs.skill.name if vs.skill else "Unknown",
                is_mandatory=vs.is_mandatory if vs.is_mandatory is not None else True,
            )
            for vs in vacancy_skills
        ]

    company_info = CompanyInfo(
        id=vacancy.company.id,
        name=vacancy.company.name,
        industry=vacancy.company.industry,
        website_url=vacancy.company.website_url,
    )

    return GetVacancyResult(
        vacancy=VacancyDetailResponse(
            id=vacancy.id,
            company=company_info,
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
            is_scraped=vacancy.is_scraped if vacancy.is_scraped is not None else False,
            is_auto_close=vacancy.is_auto_close if vacancy.is_auto_close is not None else True,
            is_active=vacancy.is_active if vacancy.is_active is not None else True,
            skills=skills,
            created_at=vacancy.created_at,
            updated_at=vacancy.updated_at,
        )
    )
