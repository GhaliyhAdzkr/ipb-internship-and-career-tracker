"""
Company Router - API endpoints untuk company/mitra operations
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app_backend.features.company import (
    GetCompanyDetailCommand,
    get_company_detail_command_handler,
)
from app_backend.schemas.company import CompanyDetailResponse
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import get_current_active_user
from app_backend.domain.user import User as DomainUser

router = APIRouter(
    prefix="/api/v1/companies",
    tags=["companies"]
)


@router.get("/{company_id}", response_model=CompanyDetailResponse)
async def get_company_detail(
    company_id: UUID,
    current_user: DomainUser = Depends(get_current_active_user),
    session=Depends(get_session),
) -> CompanyDetailResponse:
    """
    Mendapatkan detail perusahaan mitra
    
    Data yang dikembalikan:
    - Nama perusahaan
    - Industri
    - Website
    - Alamat
    - Status verifikasi
    
    Endpoint ini bisa diakses oleh semua user yang sudah login
    (mahasiswa bisa melihat info perusahaan sebelum melamar)
    """
    
    result = get_company_detail_command_handler(
        command=GetCompanyDetailCommand(company_id=company_id),
        session=session,
    )
    
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=result.error_message
        )
    
    return result.company


# TODO: Implement POST /companies/review (Future Feature)
# Endpoint untuk mahasiswa memberi review anonim terhadap tempat magang
# @router.post("/review", status_code=HTTPStatus.CREATED)
# async def create_company_review(
#     review_data: CompanyReviewCreate,
#     current_user: DomainUser = Depends(get_current_active_user),
#     session=Depends(get_session),
# ) -> CompanyReviewResponse:
#     """
#     Membuat review anonim untuk perusahaan tempat magang
#     
#     Fitur ini untuk masa depan, memerlukan:
#     - Tabel company_reviews di database
#     - Validasi mahasiswa sudah selesai magang di perusahaan tersebut
#     - Anonymization logic
#     """
#     pass
