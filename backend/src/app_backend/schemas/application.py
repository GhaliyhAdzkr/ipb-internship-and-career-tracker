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
