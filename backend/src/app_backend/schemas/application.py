import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    vacancy_id: uuid.UUID


class ApplicationLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
    new_status: str
    previous_status: Optional[str] = None
    changed_by: Optional[uuid.UUID] = None
    proof_url: Optional[str] = None
    reason: Optional[str] = None
    created_at: Optional[datetime] = None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vacancy_id: uuid.UUID
    student_id: uuid.UUID
    cv_snapshot_url: str
    status: str


class VacancyMinimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    type: str
    location: Optional[str] = None
    payment_type: Optional[str] = None
    company_name: str
    company_logo: Optional[str] = None


class ApplicationDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vacancy_id: uuid.UUID
    student_id: uuid.UUID
    cv_snapshot_url: str
    status: str
    match_percentage: Optional[float] = None
    applied_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    vacancy: Optional[VacancyMinimalResponse] = None


class ApplicationUpdateStatus(BaseModel):
    status: str
    reason: str | None = None
    proof_url: str | None = None


class ApplicationVerifyPayload(BaseModel):
    start_date: date
    end_date: date


class ApplicationRejectPayload(BaseModel):
    reason: str
