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
