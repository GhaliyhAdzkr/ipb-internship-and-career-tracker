from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app_backend.features.application.initialize_apply import (
    InitializeApplyCommand,
    initialize_apply_command_handler,
)
from app_backend.schemas.application import ApplicationCreate, ApplicationResponse
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import require_student

router = APIRouter(prefix="/api/v1/applications", tags=["applications"])

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def initialize_apply(
  payload: ApplicationCreate,
  current_user=Depends(require_student),
  session: Session = Depends(get_session),
):
    result = initialize_apply_command_handler(
        command=InitializeApplyCommand(
            payload=payload,
            student_id=current_user.id,
        ),
        session=session,
    )

    if result.error_message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error_message)

    return result.application