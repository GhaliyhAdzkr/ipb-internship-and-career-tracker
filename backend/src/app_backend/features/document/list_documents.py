import uuid
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy.orm import Session

from app_backend.models.document_requests import DocumentRequests
from app_backend.schemas.document import DocumentResponse


@dataclass
class ListDocumentsCommand:
    student_id: uuid.UUID


@dataclass
class ListDocumentsResult:
    documents: List[DocumentResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_documents_command_handler(command: ListDocumentsCommand, session: Session) -> ListDocumentsResult:
    docs = (
        session.query(DocumentRequests)
        .filter(DocumentRequests.student_id == command.student_id)
        .order_by(DocumentRequests.created_at.desc())
        .all()
    )

    return ListDocumentsResult(documents=[DocumentResponse.model_validate(d) for d in docs])
