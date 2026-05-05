import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app_backend.features.placement import (
    CreateActivityLogCommand, DeleteActivityLogCommand, GetMyPlacementsCommand,
    ListActivityLogsCommand, UpdateActivityLogCommand,
    UploadActivityLogAttachmentCommand, create_activity_log_command_handler,
    delete_activity_log_command_handler, get_my_placements_command_handler,
    list_activity_logs_command_handler, update_activity_log_command_handler,
    upload_activity_log_attachment_command_handler)
from app_backend.features.placement.generate_report import (
    GenerateReportCommand, generate_report_command_handler)
from app_backend.features.placement.get_report import (
    GetReportCommand, get_report_command_handler)
from app_backend.schemas.placement import (ActivityLogCreate,
                                           ActivityLogResponse,
                                           ActivityLogUpdate,
                                           PlacementResponse)
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import require_student

router = APIRouter(prefix="/api/v1/placements", tags=["placements"])


@router.get(
    "/me",
    response_model=List[PlacementResponse],
    summary="Mahasiswa melihat data penempatan aktifnya",
)
def get_my_placements(
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = get_my_placements_command_handler(
        command=GetMyPlacementsCommand(student_id=current_user.id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error_message
        )
    return result.placements


@router.get(
    "/{placement_id}/logs",
    response_model=List[ActivityLogResponse],
    summary="Daftar log harian",
)
def list_activity_logs(
    placement_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = list_activity_logs_command_handler(
        command=ListActivityLogsCommand(
            placement_id=placement_id, student_id=current_user.id
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.error_message
        )
    return result.logs


@router.post(
    "/{placement_id}/logs",
    response_model=ActivityLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mahasiswa menginput log harian",
)
def create_activity_log(
    placement_id: uuid.UUID,
    payload: ActivityLogCreate,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = create_activity_log_command_handler(
        command=CreateActivityLogCommand(
            placement_id=placement_id,
            student_id=current_user.id,
            log_date=payload.log_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
            description_raw=payload.description_raw,
        ),
        session=session,
    )
    if result.got_error():
        err_status = (
            status.HTTP_400_BAD_REQUEST
            if result.error_code == 400
            else result.error_code
        )
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return result.log


@router.patch(
    "/{placement_id}/logs/{log_id}",
    response_model=ActivityLogResponse,
    summary="Edit log yang sudah ada",
)
def update_activity_log(
    placement_id: uuid.UUID,
    log_id: uuid.UUID,
    payload: ActivityLogUpdate,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = update_activity_log_command_handler(
        command=UpdateActivityLogCommand(
            placement_id=placement_id,
            log_id=log_id,
            student_id=current_user.id,
            log_date=payload.log_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
            description_raw=payload.description_raw,
        ),
        session=session,
    )
    if result.got_error():
        err_status = (
            status.HTTP_400_BAD_REQUEST
            if result.error_code == 400
            else result.error_code
        )
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return result.log


@router.delete(
    "/{placement_id}/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hapus log",
)
def delete_activity_log(
    placement_id: uuid.UUID,
    log_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = delete_activity_log_command_handler(
        command=DeleteActivityLogCommand(
            placement_id=placement_id,
            log_id=log_id,
            student_id=current_user.id,
        ),
        session=session,
    )
    if result.got_error():
        err_status = (
            status.HTTP_400_BAD_REQUEST
            if result.error_code == 400
            else result.error_code
        )
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return


@router.post(
    "/{placement_id}/logs/{log_id}/attachment", summary="Upload lampiran log harian"
)
def upload_activity_log_attachment(
    placement_id: uuid.UUID,
    log_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = upload_activity_log_attachment_command_handler(
        command=UploadActivityLogAttachmentCommand(
            placement_id=placement_id,
            log_id=log_id,
            student_id=current_user.id,
            file=file,
        ),
        session=session,
    )
    if result.got_error():
        err_status = result.error_code if hasattr(result, 'error_code') and result.error_code else status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=err_status, detail=result.error_message
        )
    return {"message": result.message, "attachment_url": result.attachment_url}


@router.post("/{placement_id}/report/generate", status_code=status.HTTP_202_ACCEPTED)
def generate_report(
    placement_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = generate_report_command_handler(
        command=GenerateReportCommand(
            placement_id=placement_id, student_id=current_user.id
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=result.error_status_code, detail=result.error_message
        )
    return {"message": result.message}


@router.get("/{placement_id}/report")
def get_report(
    placement_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = get_report_command_handler(
        command=GetReportCommand(placement_id=placement_id, student_id=current_user.id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=result.error_status_code, detail=result.error_message
        )
    return {
        "status": result.status,
        "auto_generated_report_url": result.auto_generated_report_url,
    }
