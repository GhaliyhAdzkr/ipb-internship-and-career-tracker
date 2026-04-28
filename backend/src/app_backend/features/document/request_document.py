import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.document_requests import DocumentRequests
from app_backend.shared.tasks.report_tasks import generate_cover_letter


@dataclass
class RequestDocumentCommand:
    student_id: uuid.UUID
    document_type: str
    purpose: str
    reference_vacancy_id: Optional[uuid.UUID] = None


@dataclass
class RequestDocumentResult:
    document_id: Optional[uuid.UUID] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
    error_status_code: int = 400

    def got_error(self) -> bool:
        return self.error_message is not None


def request_document_command_handler(
    command: RequestDocumentCommand, session: Session
) -> RequestDocumentResult:
    doc_req = DocumentRequests(
        student_id=command.student_id,
        document_type=command.document_type,
        purpose=command.purpose,
        reference_vacancy_id=command.reference_vacancy_id,
        status="PENDING",
    )
    session.add(doc_req)
    session.commit()
    session.refresh(doc_req)

    # Trigger background task
    generate_cover_letter.delay(str(doc_req.id))

    return RequestDocumentResult(
        document_id=doc_req.id,
        message="Permohonan surat berhasil diajukan dan sedang diproses",
    )
