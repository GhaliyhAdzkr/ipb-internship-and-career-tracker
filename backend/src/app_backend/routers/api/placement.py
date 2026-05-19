import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app_backend.features.placement import (
    DeleteActivityLogCommand,
    UpdateActivityLogCommand,
    UploadActivityLogAttachmentCommand,
    delete_activity_log_command_handler,
    update_activity_log_command_handler,
    upload_activity_log_attachment_command_handler,
)
from app_backend.features.placement.generate_report import GenerateReportCommand, generate_report_command_handler
from app_backend.features.placement.get_report import GetReportCommand, get_report_command_handler
from app_backend.features.placement.placement_service import PlacementService
from app_backend.models.activity_logs import ActivityLogs
from app_backend.models.placements import Placements
from app_backend.schemas.placement import ActivityLogCreate, ActivityLogResponse, ActivityLogUpdate, PlacementResponse
from app_backend.shared.auth_dependencies import require_student
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import get_placement_service
from app_backend.shared.tasks.ai_tasks import enhance_log_description

router = APIRouter(prefix="/api/v1/placements", tags=["placements"])


@router.get(
    "/me",
    response_model=List[PlacementResponse],
    summary="Mahasiswa melihat data penempatan aktifnya",
)
def get_my_placements(
    current_user=Depends(require_student),
    placement_service: PlacementService = Depends(get_placement_service),
):
    return placement_service.get_my_placements(current_user.id)


@router.get(
    "/{placement_id}/logs",
    response_model=List[ActivityLogResponse],
    summary="Daftar log harian",
)
def list_activity_logs(
    placement_id: uuid.UUID,
    current_user=Depends(require_student),
    placement_service: PlacementService = Depends(get_placement_service),
):
    try:
        return placement_service.list_activity_logs(placement_id, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


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
    placement_service: PlacementService = Depends(get_placement_service),
):
    try:
        return placement_service.create_activity_log(current_user.id, placement_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal membuat log: {exc}",
        )


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
        err_status = status.HTTP_400_BAD_REQUEST if result.error_code == 400 else result.error_code
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
        err_status = status.HTTP_400_BAD_REQUEST if result.error_code == 400 else result.error_code
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return


@router.post("/{placement_id}/logs/{log_id}/attachment", summary="Upload lampiran log harian")
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
        err_status = result.error_code if hasattr(result, "error_code") and result.error_code else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return {"message": result.message, "attachment_url": result.attachment_url}


@router.post(
    "/{placement_id}/logs/{log_id}/enhance",
    response_model=ActivityLogResponse,
    summary="Poles deskripsi jurnal harian dengan AI",
)
def enhance_activity_log_description(
    placement_id: uuid.UUID,
    log_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    placement = session.query(Placements).filter_by(id=placement_id, student_id=current_user.id).first()
    if not placement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Placement tidak ditemukan")

    log = session.query(ActivityLogs).filter_by(id=log_id, placement_id=placement.id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity log tidak ditemukan")

    task_result = enhance_log_description(str(log.id), log.description_raw)
    if not task_result.get("success"):
        error = task_result.get("error") or "Gagal memoles deskripsi jurnal"
        err_status = status.HTTP_429_TOO_MANY_REQUESTS if "Rate limit" in error else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=err_status, detail=error)

    enhanced = (task_result.get("result") or {}).get("enhanced")
    if not enhanced:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI tidak mengembalikan hasil enhancement")

    log.description_ai_enhanced = enhanced
    session.commit()
    session.refresh(log)
    return log


@router.post("/{placement_id}/report/generate", status_code=status.HTTP_202_ACCEPTED)
def generate_report(
    placement_id: uuid.UUID,
    current_user=Depends(require_student),
    session: Session = Depends(get_session),
):
    result = generate_report_command_handler(
        command=GenerateReportCommand(placement_id=placement_id, student_id=current_user.id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(status_code=result.error_status_code, detail=result.error_message)
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
        raise HTTPException(status_code=result.error_status_code, detail=result.error_message)
    return {
        "status": result.status,
        "auto_generated_report_url": result.auto_generated_report_url,
    }
