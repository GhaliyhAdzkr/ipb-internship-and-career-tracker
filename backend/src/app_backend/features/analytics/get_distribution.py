import uuid
from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy import case, extract, func
from sqlalchemy.orm import Session

from app_backend.models.applications import Applications
from app_backend.models.master_departments import MasterDepartments
from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.models.placements import Placements
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.vacancies import Vacancies


@dataclass
class GetDistributionCommand:
    department_id: Optional[uuid.UUID] = None
    year: Optional[int] = None


@dataclass
class TopCompanyData:
    company_id: uuid.UUID
    company_name: str
    company_industry: Optional[str]
    total_students: int


@dataclass
class DepartmentBreakdownData:
    department_id: uuid.UUID
    department_name: str
    department_code: str
    company_id: uuid.UUID
    company_name: str
    total_students: int


@dataclass
class CompensationBreakdownData:
    payment_type: str
    total: int


@dataclass
class SemesterTrendData:
    year: int
    semester: int  # 1 = Genap (Jan-Jun), 2 = Ganjil (Jul-Des)
    total: int


@dataclass
class GetDistributionResult:
    top_companies: List[TopCompanyData] = field(default_factory=list)
    department_breakdown: List[DepartmentBreakdownData] = field(default_factory=list)
    compensation_breakdown: List[CompensationBreakdownData] = field(default_factory=list)
    semester_trends: List[SemesterTrendData] = field(default_factory=list)
    total_placements: int = 0
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def _apply_filters(query, command: GetDistributionCommand):
    if command.department_id:
        query = query.filter(ProfilesStudent.department_id == command.department_id)
    if command.year:
        query = query.filter(extract("year", Placements.start_date) == command.year)
    return query


def get_distribution_command_handler(
    command: GetDistributionCommand,
    session: Session,
) -> GetDistributionResult:

    total_query = session.query(func.count(Placements.id)).join(ProfilesStudent, Placements.student_id == ProfilesStudent.user_id)
    total_query = _apply_filters(total_query, command)
    total_placements = total_query.scalar() or 0

    top_co_query = (
        session.query(
            MasterExternalCompanies.id,
            MasterExternalCompanies.name,
            MasterExternalCompanies.industry,
            func.count(Placements.id).label("total_students"),
        )
        .join(Placements, Placements.company_id == MasterExternalCompanies.id)
        .join(ProfilesStudent, Placements.student_id == ProfilesStudent.user_id)
    )
    top_co_query = _apply_filters(top_co_query, command)
    top_co_rows = (
        top_co_query.group_by(
            MasterExternalCompanies.id,
            MasterExternalCompanies.name,
            MasterExternalCompanies.industry,
        )
        .order_by(func.count(Placements.id).desc())
        .limit(10)
        .all()
    )
    top_companies = [
        TopCompanyData(
            company_id=row[0],
            company_name=row[1],
            company_industry=row[2],
            total_students=row[3],
        )
        for row in top_co_rows
    ]

    dept_query = (
        session.query(
            MasterDepartments.id,
            MasterDepartments.name,
            MasterDepartments.code,
            MasterExternalCompanies.id,
            MasterExternalCompanies.name,
            func.count(Placements.id).label("total_students"),
        )
        .join(Placements, Placements.company_id == MasterExternalCompanies.id)
        .join(ProfilesStudent, Placements.student_id == ProfilesStudent.user_id)
        .join(MasterDepartments, ProfilesStudent.department_id == MasterDepartments.id)
    )
    dept_query = _apply_filters(dept_query, command)
    dept_rows = (
        dept_query.group_by(
            MasterDepartments.id,
            MasterDepartments.name,
            MasterDepartments.code,
            MasterExternalCompanies.id,
            MasterExternalCompanies.name,
        )
        .order_by(func.count(Placements.id).desc())
        .all()
    )
    department_breakdown = [
        DepartmentBreakdownData(
            department_id=row[0],
            department_name=row[1],
            department_code=row[2],
            company_id=row[3],
            company_name=row[4],
            total_students=row[5],
        )
        for row in dept_rows
    ]

    comp_query = (
        session.query(
            Vacancies.payment_type,
            func.count(Placements.id).label("total"),
        )
        .join(ProfilesStudent, Placements.student_id == ProfilesStudent.user_id)
        .outerjoin(Applications, Placements.application_id == Applications.id)
        .outerjoin(Vacancies, Applications.vacancy_id == Vacancies.id)
    )
    comp_query = _apply_filters(comp_query, command)
    comp_rows = comp_query.group_by(Vacancies.payment_type).all()
    compensation_breakdown = [
        CompensationBreakdownData(
            payment_type=row[0] if row[0] is not None else "UNKNOWN",
            total=row[1],
        )
        for row in comp_rows
    ]

    semester_expr = case(
        (extract("month", Placements.start_date) <= 6, 1),
        else_=2,
    )
    year_expr = extract("year", Placements.start_date)

    trend_query = session.query(
        year_expr.label("year"),
        semester_expr.label("semester"),
        func.count(Placements.id).label("total"),
    ).join(ProfilesStudent, Placements.student_id == ProfilesStudent.user_id)
    trend_query = _apply_filters(trend_query, command)
    trend_rows = trend_query.group_by(year_expr, semester_expr).order_by(year_expr, semester_expr).all()
    semester_trends = [SemesterTrendData(year=int(row[0]), semester=int(row[1]), total=row[2]) for row in trend_rows]

    return GetDistributionResult(
        top_companies=top_companies,
        department_breakdown=department_breakdown,
        compensation_breakdown=compensation_breakdown,
        semester_trends=semester_trends,
        total_placements=total_placements,
    )
