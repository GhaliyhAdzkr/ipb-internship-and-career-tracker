"""
Admin Router – API endpoints untuk manajemen data master dan akun user.

Endpoints:
  PATCH /users/{user_id}/toggle-active  – Toggle aktif/nonaktif akun user
  GET   /profile/me                     – Profil admin yang sedang login
  PATCH /profile/me                     – Update profil admin

  GET    /departments          – Daftar semua prodi
  POST   /departments          – Tambah prodi baru
  PATCH  /departments/{id}     – Update prodi
  DELETE /departments/{id}     – Hapus prodi

  GET    /skills               – Daftar semua skill
  POST   /skills               – Tambah skill baru
  PATCH  /skills/{id}          – Update skill
  DELETE /skills/{id}          – Hapus skill

  GET    /companies            – Daftar semua perusahaan eksternal
  POST   /companies            – Tambah perusahaan baru
  PATCH  /companies/{id}       – Update perusahaan
  DELETE /companies/{id}       – Hapus perusahaan
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app_backend.domain.user import User as DomainUser
from app_backend.features.admin import ToggleUserActiveCommand, toggle_user_active_command_handler
from app_backend.features.admin.master_data_service import MasterDataService
from app_backend.features.application import (
    ListPendingVerificationCommand,
    RejectApplicationProofCommand,
    VerifyApplicationCommand,
    list_pending_verification_command_handler,
    reject_application_proof_command_handler,
    verify_application_command_handler,
)
from app_backend.features.placement import ListAdminPlacementsCommand, list_admin_placements_command_handler
from app_backend.models.profiles_admin import ProfilesAdmin
from app_backend.schemas.admin import (
    AdminProfileResponse,
    AdminProfileUpdate,
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app_backend.schemas.application import ApplicationRejectPayload, ApplicationResponse, ApplicationVerifyPayload
from app_backend.schemas.placement import PlacementResponse
from app_backend.schemas.user import UserResponse
from app_backend.shared.auth_dependencies import require_admin
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import get_master_data_service

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
)

# User Account Activation (Section 1.2)


@router.patch(
    "/users/{user_id}/toggle-active",
    response_model=UserResponse,
    summary="Toggle aktif/nonaktif akun user",
)
async def toggle_user_active(
    user_id: uuid.UUID,
    session=Depends(get_session),
    _: DomainUser = Depends(require_admin),
) -> UserResponse:
    """
    Admin menonaktifkan atau mengaktifkan kembali akun user.
    Toggle: `is_active = True` → `False`, dan sebaliknya.
    """
    result = toggle_user_active_command_handler(
        command=ToggleUserActiveCommand(user_id=user_id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=result.error_message)
    return result.user


# Admin Profile (Section 2.3)


@router.get(
    "/profile/me",
    response_model=AdminProfileResponse,
    summary="Profil admin yang sedang login",
)
async def get_admin_profile(
    session=Depends(get_session),
    current_user: DomainUser = Depends(require_admin),
) -> AdminProfileResponse:
    """Kembalikan data profil admin berdasarkan JWT access token."""
    profile = session.query(ProfilesAdmin).filter(ProfilesAdmin.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Profil admin tidak ditemukan",
        )
    return AdminProfileResponse(
        user_id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
        full_name=profile.full_name,
        unit_name=profile.unit_name,
        nip=profile.nip,
        last_login_at=current_user.last_login_at,
        updated_at=profile.updated_at,
    )


@router.patch(
    "/profile/me",
    response_model=AdminProfileResponse,
    summary="Update profil admin",
)
async def update_admin_profile(
    payload: AdminProfileUpdate,
    session=Depends(get_session),
    current_user: DomainUser = Depends(require_admin),
) -> AdminProfileResponse:
    """Update nama, unit kerja, atau NIP admin yang sedang login."""
    from sqlalchemy.exc import IntegrityError

    profile = session.query(ProfilesAdmin).filter(ProfilesAdmin.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Profil admin tidak ditemukan")

    try:
        if payload.full_name is not None:
            profile.full_name = payload.full_name
        if payload.unit_name is not None:
            profile.unit_name = payload.unit_name
        if payload.nip is not None:
            profile.nip = payload.nip
        profile.updated_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(profile)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"NIP '{payload.nip}' sudah digunakan oleh admin lain",
        )

    return AdminProfileResponse(
        user_id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
        full_name=profile.full_name,
        unit_name=profile.unit_name,
        nip=profile.nip,
        last_login_at=current_user.last_login_at,
        updated_at=profile.updated_at,
    )


# Manage Departments (Section 2.1)


@router.get(
    "/departments",
    response_model=List[DepartmentResponse],
    summary="Daftar semua Program Studi",
)
async def list_departments(
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> List[DepartmentResponse]:
    return master_data_service.list_departments()


@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=HTTPStatus.CREATED,
    summary="Tambah Program Studi baru",
)
async def create_department(
    payload: DepartmentCreate,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> DepartmentResponse:
    try:
        return master_data_service.create_department(payload)
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


@router.patch(
    "/departments/{dept_id}",
    response_model=DepartmentResponse,
    summary="Update Program Studi",
)
async def update_department(
    dept_id: uuid.UUID,
    payload: DepartmentUpdate,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> DepartmentResponse:
    try:
        return master_data_service.update_department(dept_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


@router.delete(
    "/departments/{dept_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Hapus Program Studi",
)
async def delete_department(
    dept_id: uuid.UUID,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> None:
    try:
        master_data_service.delete_department(dept_id)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


# Manage Skills (Section 2.1)


@router.get(
    "/skills",
    response_model=List[SkillResponse],
    summary="Daftar semua Master Skill",
)
async def list_skills(
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> List[SkillResponse]:
    return master_data_service.list_skills()


@router.post(
    "/skills",
    response_model=SkillResponse,
    status_code=HTTPStatus.CREATED,
    summary="Tambah skill baru",
)
async def create_skill(
    payload: SkillCreate,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> SkillResponse:
    try:
        return master_data_service.create_skill(payload)
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


@router.patch(
    "/skills/{skill_id}",
    response_model=SkillResponse,
    summary="Update skill",
)
async def update_skill(
    skill_id: uuid.UUID,
    payload: SkillUpdate,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> SkillResponse:
    try:
        return master_data_service.update_skill(skill_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


@router.delete(
    "/skills/{skill_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Hapus skill",
)
async def delete_skill(
    skill_id: uuid.UUID,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> None:
    try:
        master_data_service.delete_skill(skill_id)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


# Manage External Companies (Section 2.1)


@router.get(
    "/companies",
    response_model=List[CompanyResponse],
    summary="Daftar semua perusahaan eksternal",
)
async def list_companies(
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> List[CompanyResponse]:
    return master_data_service.list_companies()


@router.post(
    "/companies",
    response_model=CompanyResponse,
    status_code=HTTPStatus.CREATED,
    summary="Tambah perusahaan eksternal baru",
)
async def create_company(
    payload: CompanyCreate,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> CompanyResponse:
    try:
        return master_data_service.create_company(payload)
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


@router.patch(
    "/companies/{company_id}",
    response_model=CompanyResponse,
    summary="Update perusahaan eksternal",
)
async def update_company(
    company_id: uuid.UUID,
    payload: CompanyUpdate,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> CompanyResponse:
    try:
        return master_data_service.update_company(company_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


@router.delete(
    "/companies/{company_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Hapus perusahaan eksternal",
)
async def delete_company(
    company_id: uuid.UUID,
    master_data_service: MasterDataService = Depends(get_master_data_service),
    _: DomainUser = Depends(require_admin),
) -> None:
    try:
        master_data_service.delete_company(company_id)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc))


# Manage Applications (Section 4)


@router.get(
    "/applications/pending-verification",
    response_model=List[ApplicationResponse],
    summary="Daftar lamaran pending verifikasi",
)
async def list_pending_verification(
    session=Depends(get_session),
    _: DomainUser = Depends(require_admin),
) -> List[ApplicationResponse]:
    result = list_pending_verification_command_handler(ListPendingVerificationCommand(), session)
    if result.got_error():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result.error_message)
    return result.items


@router.post(
    "/applications/{application_id}/verify",
    summary="Verifikasi dan buat placement",
)
async def verify_application(
    application_id: uuid.UUID,
    payload: ApplicationVerifyPayload,
    session=Depends(get_session),
    current_admin: DomainUser = Depends(require_admin),
):
    result = verify_application_command_handler(
        VerifyApplicationCommand(
            application_id=application_id,
            admin_id=current_admin.id,
            start_date=payload.start_date,
            end_date=payload.end_date,
        ),
        session,
    )
    if result.got_error():
        err_status = result.error_code if hasattr(result, "error_code") and result.error_code else HTTPStatus.BAD_REQUEST
        raise HTTPException(status_code=err_status, detail=result.error_message)
    return {"message": "Placement berhasil dibuat", "placement_id": result.placement.id}


@router.post(
    "/applications/{application_id}/reject-proof",
    response_model=ApplicationResponse,
    summary="Tolak bukti dan kembalikan ke OFFERED",
)
async def reject_application_proof(
    application_id: uuid.UUID,
    payload: ApplicationRejectPayload,
    session=Depends(get_session),
    current_admin: DomainUser = Depends(require_admin),
):
    result = reject_application_proof_command_handler(
        RejectApplicationProofCommand(
            application_id=application_id,
            admin_id=current_admin.id,
            reason=payload.reason,
        ),
        session,
    )
    if result.got_error():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result.error_message)
    return result.application


# Manage Placements (Section 5)


@router.get(
    "/placements",
    response_model=List[PlacementResponse],
    summary="Daftar semua penempatan",
)
async def list_admin_placements(
    session=Depends(get_session),
    _: DomainUser = Depends(require_admin),
) -> List[PlacementResponse]:
    result = list_admin_placements_command_handler(ListAdminPlacementsCommand(), session)
    if result.got_error():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result.error_message)
    return result.placements
