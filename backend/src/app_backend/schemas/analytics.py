import uuid
from typing import List, Optional

from pydantic import BaseModel


class TopCompanyItem(BaseModel):
    company_id: uuid.UUID
    company_name: str
    company_industry: Optional[str] = None
    total_students: int


class DepartmentBreakdownItem(BaseModel):
    department_id: uuid.UUID
    department_name: str
    department_code: str
    company_id: uuid.UUID
    company_name: str
    total_students: int


class CompensationBreakdownItem(BaseModel):
    payment_type: str
    total: int


class SemesterTrendItem(BaseModel):
    year: int
    semester: int
    total: int


class DistributionResponse(BaseModel):
    total_placements: int
    top_companies: List[TopCompanyItem]
    department_breakdown: List[DepartmentBreakdownItem]
    compensation_breakdown: List[CompensationBreakdownItem]
    semester_trends: List[SemesterTrendItem]
    applied_filters: dict


class StatusBreakdownItem(BaseModel):
    status: str
    total: int


class ApplicationStatsResponse(BaseModel):
    total_applications: int
    status_breakdown: List[StatusBreakdownItem]
    conversion_rate: float


class TopVacancyItem(BaseModel):
    vacancy_id: uuid.UUID
    title: str
    company_id: uuid.UUID
    total_applicants: int


class VacancyStatsResponse(BaseModel):
    total_active_vacancies: int
    avg_applicants_per_vacancy: float
    top_vacancies: List[TopVacancyItem]
