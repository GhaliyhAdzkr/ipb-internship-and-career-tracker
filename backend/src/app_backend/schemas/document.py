import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentRequestPayload(BaseModel):
    document_type: str
    purpose: str
    reference_vacancy_id: Optional[uuid.UUID] = None


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    document_type: str
    purpose: Optional[str] = None
    reference_vacancy_id: Optional[uuid.UUID] = None
    generated_url: Optional[str] = None
    status: str
    created_at: datetime
