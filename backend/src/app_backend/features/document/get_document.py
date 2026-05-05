from http import HTTPStatus
import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.document_requests import DocumentRequests
from app_backend.schemas.document import DocumentResponse


@dataclass
class GetDocumentCommand:
    student_id: uuid.UUID
    document_id: uuid.UUID


@dataclass
class GetDocumentResult:
    document: Optional[DocumentResponse] = None
    error_message: Optional[str] = None
    error_status_code: HTTPStatus = HTTPStatus.BAD_REQUEST

    def got_error(self) -> bool:
        return self.error_message is not None


def get_document_command_handler(
    command: GetDocumentCommand, session: Session
) -> GetDocumentResult:
    doc = (
        session.query(DocumentRequests)
        .filter(
            DocumentRequests.id == command.document_id,
            DocumentRequests.student_id == command.student_id,
        )
        .first()
    )

    if not doc:
        return GetDocumentResult(error_message="Dokumen tidak ditemukan")

    return GetDocumentResult(document=DocumentResponse.model_validate(doc))
