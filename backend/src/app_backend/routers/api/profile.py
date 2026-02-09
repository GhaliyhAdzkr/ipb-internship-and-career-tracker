"""
Profile Router - API endpoints untuk student profile
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app_backend.features.profile import (
    GetStudentProfileCommand,
    get_student_profile_command_handler,
    UpdateCVDataCommand,
    update_cv_data_command_handler,
)
from app_backend.schemas.profile import StudentProfileResponse, CVDataUpdate
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import get_current_active_user
from app_backend.domain.user import User as DomainUser

router = APIRouter(
    prefix="/api/v1/profile",
    tags=["profile"]
)


@router.get("/me", response_model=StudentProfileResponse)
async def get_my_profile(
    current_user: DomainUser = Depends(get_current_active_user),
    session=Depends(get_session),
) -> StudentProfileResponse:
    """
    Mengambil data profil mahasiswa yang sedang login
    
    Data yang dikembalikan:
    - Data akademik (NIM, Jurusan, IPK, Semester, SKS)
    - Data CV (Telepon, LinkedIn, CV URL)
    - Skills dengan level
    
    Endpoint ini hanya untuk mahasiswa (role STUDENT)
    """
    
    # Validasi role
    if current_user.role != "STUDENT":
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Endpoint ini hanya untuk mahasiswa"
        )
    
    result = get_student_profile_command_handler(
        command=GetStudentProfileCommand(user_id=current_user.id),
        session=session,
    )
    
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=result.error_message
        )
    
    return result.profile


@router.put("/cv-data", status_code=HTTPStatus.OK)
async def update_cv_data(
    cv_data: CVDataUpdate,
    current_user: DomainUser = Depends(get_current_active_user),
    session=Depends(get_session),
) -> dict:
    """
    Update data CV mahasiswa (Skill, Pengalaman, Kontak)
    
    Data yang bisa diupdate:
    - phone_number: Nomor telepon
    - linkedin_url: URL profil LinkedIn
    - cv_url: URL file CV (Google Drive, Dropbox, dll)
    - skills: Daftar skills dengan level 1-5
    
    Endpoint ini hanya untuk mahasiswa (role STUDENT)
    
    Catatan:
    - Data akademik (NIM, Jurusan, IPK) tidak bisa diubah melalui endpoint ini
    - Data akademik diambil langsung dari database IPB
    """
    
    # Validasi role
    if current_user.role != "STUDENT":
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Endpoint ini hanya untuk mahasiswa"
        )
    
    result = update_cv_data_command_handler(
        command=UpdateCVDataCommand(
            user_id=current_user.id,
            payload=cv_data
        ),
        session=session,
    )
    
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message
        )
    
    return {"message": result.message}
