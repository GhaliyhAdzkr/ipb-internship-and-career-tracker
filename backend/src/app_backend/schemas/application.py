import uuid
from datetime import datetime
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


class ApplicationUpdateStatus(BaseModel):
    status: str
    reason: str | None = None
    proof_url: str | None = None


import datetime


class ApplicationVerifyPayload(BaseModel):
    start_date: datetime.date
    end_date: datetime.date


class ApplicationRejectPayload(BaseModel):
    reason: str
