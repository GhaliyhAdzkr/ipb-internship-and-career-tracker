from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session, joinedload, selectinload

from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills
from app_backend.schemas.vacancy import CompanyInfo, SkillRequirement, VacancyDetailResponse, VacancyListResponse


class ListVacanciesException(Exception):
    pass


@dataclass
class ListVacanciesCommand:
    page: int = 1
    per_page: int = 10
    is_active: bool = True


@dataclass
class ListVacanciesResult:
    data: Optional[VacancyListResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_vacancies_command_handler(
    command: ListVacanciesCommand,
    session: Session,
) -> ListVacanciesResult:
    """
    List vacancies dengan pagination.
    """
    page = max(1, command.page)
    per_page = min(max(1, command.per_page), 100)  # Max 100 per page
    offset = (page - 1) * per_page

    # Base query
    query = session.query(Vacancies).options(
        joinedload(Vacancies.company),
        selectinload(Vacancies.vacancy_skills).joinedload(VacancySkills.skill),
    )

    # Filter active only
    if command.is_active is not None:
        query = query.filter(Vacancies.is_active == command.is_active)

    # Get total count
    total = query.count()

    # Get paginated results
    vacancies = query.order_by(Vacancies.created_at.desc()).offset(offset).limit(per_page).all()

    # Build response with skills
    items = []
    for vacancy in vacancies:
        # Get skills from eagerly loaded relationship
        vacancy_skills = vacancy.vacancy_skills
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

        items.append(
            VacancyDetailResponse(
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

    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return ListVacanciesResult(
        data=VacancyListResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )
    )
