import uuid
from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app_backend.models.applications import Applications
from app_backend.models.vacancies import Vacancies


@dataclass
class GetVacancyStatsCommand:
    pass


@dataclass
class TopVacancyData:
    vacancy_id: uuid.UUID
    title: str
    company_id: uuid.UUID
    total_applicants: int


@dataclass
class GetVacancyStatsResult:
    total_active_vacancies: int = 0
    avg_applicants_per_vacancy: float = 0.0
    top_vacancies: List[TopVacancyData] = field(default_factory=list)
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def get_vacancy_stats_command_handler(
    command: GetVacancyStatsCommand,
    session: Session,
) -> GetVacancyStatsResult:

    total_active = session.query(func.count(Vacancies.id)).filter(Vacancies.is_active.is_(True)).scalar() or 0

    subquery = (
        session.query(func.count(Applications.id).label("cnt"))
        .group_by(Applications.vacancy_id)
        .subquery()
    )
    avg_row = session.query(func.avg(subquery.c.cnt)).scalar()
    avg_applicants = round(float(avg_row), 2) if avg_row is not None else 0.0

    top_rows = (
        session.query(
            Vacancies.id,
            Vacancies.title,
            Vacancies.company_id,
            func.count(Applications.id).label("total_applicants"),
        )
        .outerjoin(Applications, Applications.vacancy_id == Vacancies.id)
        .group_by(Vacancies.id, Vacancies.title, Vacancies.company_id)
        .order_by(func.count(Applications.id).desc())
        .limit(5)
        .all()
    )
    top_vacancies = [
        TopVacancyData(
            vacancy_id=row[0],
            title=row[1],
            company_id=row[2],
            total_applicants=row[3],
        )
        for row in top_rows
    ]

    return GetVacancyStatsResult(
        total_active_vacancies=total_active,
        avg_applicants_per_vacancy=avg_applicants,
        top_vacancies=top_vacancies,
    )
