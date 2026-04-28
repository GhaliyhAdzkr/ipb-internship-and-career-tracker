import uuid
from pydantic import BaseModel, ConfigDict

class ApplicationCreate(BaseModel):
    vacancy_id: uuid.UUID

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

class ApplicationLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
    new_status: str
    previous_status: str | None = None
    proof_url: str | None = None
    reason: str | None = None
    changed_by: uuid.UUID | None = None

import datetime

class ApplicationVerifyPayload(BaseModel):
    start_date: datetime.date
    end_date: datetime.date

class ApplicationRejectPayload(BaseModel):
    reason: str
