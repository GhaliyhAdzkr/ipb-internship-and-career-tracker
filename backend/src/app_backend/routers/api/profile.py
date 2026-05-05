"""
Profile Router – API endpoints untuk manajemen profil mahasiswa.

Endpoints:
  GET /me          – Profil lengkap mahasiswa yang sedang login
  PUT /cv-data     – Update info kontak, URL CV, dan skills
"""

from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app_backend.domain.user import User as DomainUser
from app_backend.features.profile import (GetStudentProfileCommand,
                                          UpdateCVDataCommand, UploadCVCommand,
                                          get_student_profile_command_handler,
                                          update_cv_data_command_handler,
                                          upload_cv_command_handler)
from app_backend.schemas.profile import CVDataUpdate, StudentProfileResponse
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import require_student

router = APIRouter(
    prefix="/api/v1/profile",
    tags=["profile"],
)


from app_backend.features.profile.profile_service import ProfileService
from app_backend.shared.dependencies_service import get_profile_service


@router.get(
    "/me",
    response_model=StudentProfileResponse,
    summary="Profil lengkap mahasiswa yang sedang login",
)
async def get_my_profile(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: DomainUser = Depends(require_student),
) -> StudentProfileResponse:
    """
    Kembalikan profil lengkap mahasiswa:
    - Data akademik: NIM, nama, semester, IPK, prodi
    - Data kontak: telepon, LinkedIn, URL CV
    - Skills dengan level expertise (1=Beginner … 5=Expert)

    Hanya dapat diakses oleh **STUDENT**.
    """
    profile = profile_service.get_student_profile(current_user.id)
    if not profile:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Profil mahasiswa tidak ditemukan",
        )
    return profile


@router.put(
    "/cv-data",
    status_code=HTTPStatus.OK,
    summary="Update data CV mahasiswa",
)
async def update_cv_data(
    cv_data: CVDataUpdate,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: DomainUser = Depends(require_student),
) -> dict:
    """
    Update data CV mahasiswa (PATCH semantics).

    - **phone_number**: Nomor telepon (opsional)
    - **linkedin_url**: URL profil LinkedIn (opsional)
    - **cv_url**: URL file CV – Google Drive, Dropbox, dll (opsional)
    - **skills**: Daftar skills dengan level 1–5. Jika dikirim,
      **menggantikan seluruh skills** yang sudah ada (full replace).

    Field yang tidak dikirim tidak akan diubah.
    Data akademik (NIM, prodi, IPK) tidak dapat diubah melalui endpoint ini.

    Hanya dapat diakses oleh **STUDENT**.
    """
    try:
        profile_service.update_cv_data(current_user.id, cv_data)
        return {"message": "Data CV berhasil diperbarui"}
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Update gagal: {exc}",
        )


@router.post(
    "/student/cv",
    status_code=HTTPStatus.OK,
    summary="Upload CV mahasiswa",
)
async def upload_cv(
    file: UploadFile = File(...),
    session=Depends(get_session),
    current_user: DomainUser = Depends(require_student),
) -> dict:
    """
    Upload CV mahasiswa dalam format PDF.
    - **file**: File PDF CV (max 5MB, format aplikasi PDF).
    """
    result = upload_cv_command_handler(
        command=UploadCVCommand(
            user_id=current_user.id,
            file=file,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return {"message": result.message, "cv_url": result.cv_url}
