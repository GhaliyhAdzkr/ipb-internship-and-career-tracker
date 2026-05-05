import uuid
from dataclasses import dataclass
from http import HTTPStatus
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
    error_status_code: HTTPStatus = HTTPStatus.BAD_REQUEST

    def got_error(self) -> bool:
        return self.error_message is not None


def request_document_command_handler(
    command: RequestDocumentCommand, session: Session
) -> RequestDocumentResult:
    from datetime import datetime, timedelta, timezone

    # Rate Limiting: 1 request per 5 minutes per document type
    five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
    recent_request = (
        session.query(DocumentRequests)
        .filter(
            DocumentRequests.student_id == command.student_id,
            DocumentRequests.document_type == command.document_type,
            DocumentRequests.created_at >= five_minutes_ago,
        )
        .first()
    )

    if recent_request:
        return RequestDocumentResult(
            error_message="Harap tunggu 5 menit sebelum mengajukan permohonan surat baru.",
            error_status_code=HTTPStatus.TOO_MANY_REQUESTS,
        )

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
