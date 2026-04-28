import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app_backend.features.document.get_document import (
    GetDocumentCommand, get_document_command_handler)
from app_backend.features.document.list_documents import (
    ListDocumentsCommand, list_documents_command_handler)
from app_backend.features.document.request_document import (
    RequestDocumentCommand, request_document_command_handler)
from app_backend.schemas.document import (DocumentRequestPayload,
                                          DocumentResponse)
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import require_student

router = APIRouter(prefix="/api/v1/document-requests", tags=["Documents"])


@router.post("", status_code=status.HTTP_201_CREATED)
def request_document(
    payload: DocumentRequestPayload,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = request_document_command_handler(
        command=RequestDocumentCommand(
            student_id=current_user.id,
            document_type=payload.document_type,
            purpose=payload.purpose,
            reference_vacancy_id=payload.reference_vacancy_id,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=result.error_status_code, detail=result.error_message
        )
    return {"message": result.message, "document_id": result.document_id}


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = list_documents_command_handler(
        command=ListDocumentsCommand(student_id=current_user.id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error_message
        )
    return result.documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = get_document_command_handler(
        command=GetDocumentCommand(student_id=current_user.id, document_id=document_id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=result.error_status_code, detail=result.error_message
        )
    return result.document
