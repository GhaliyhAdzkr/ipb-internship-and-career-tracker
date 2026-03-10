"""
Vacancy Router – API endpoints untuk vacancy management dan job discovery.

Endpoints:
  POST /vacancies           – Buat lowongan baru (admin only)
  GET /vacancies            – List semua lowongan aktif
  GET /vacancies/search     – Cari lowongan dengan filter
  GET /vacancies/{id}       – Detail lowongan
  PUT /vacancies/{id}       – Update lowongan (admin only)
  DELETE /vacancies/{id}    – Hapus lowongan (admin only)
  POST /wishlist            – Simpan ke wishlist
  GET /wishlist             – List wishlist student
  GET /wishlist/{id}        – Detail wishlist
  PUT /wishlist/{id}        – Update catatan wishlist
  DELETE /wishlist/{id}     – Hapus wishlist
"""

from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import parse_obj_as

from app_backend.domain.user import User as DomainUser
from app_backend.domain.student import Student as DomainStudent
from app_backend.features.vacancy import (
    CreateVacancyCommand,
    CreateVacancyResult,
    DeleteVacancyCommand,
    DeleteVacancyResult,
    GetVacancyCommand,
    GetVacancyResult,
    ListVacanciesCommand,
    ListVacanciesResult,
    SearchVacanciesCommand,
    SearchVacanciesResult,
    UpdateVacancyCommand,
    UpdateVacancyResult,
    create_vacancy_command_handler,
    delete_vacancy_command_handler,
    get_vacancy_command_handler,
    list_vacancies_command_handler,
    search_vacancies_command_handler,
    update_vacancy_command_handler,
)
from app_backend.features.wishlist import (
    AddWishlistCommand,
    AddWishlistResult,
    DeleteWishlistCommand,
    DeleteWishlistResult,
    GetWishlistCommand,
    GetWishlistResult,
    ListWishlistCommand,
    ListWishlistResult,
    UpdateWishlistCommand,
    UpdateWishlistResult,
    add_wishlist_command_handler,
    delete_wishlist_command_handler,
    get_wishlist_command_handler,
    list_wishlist_command_handler,
    update_wishlist_command_handler,
)
from app_backend.schemas.vacancy import (
    VacancyCreate,
    VacancyDetailResponse,
    VacancyListResponse,
    VacancyResponse,
    VacancySearchFilter,
    VacancyUpdate,
    VacancyType,
    PaymentType,
)
from app_backend.schemas.wishlist import (
    WishlistCreate,
    WishlistDetailResponse,
    WishlistListResponse,
    WishlistResponse,
    WishlistUpdate,
)
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import (
    get_current_active_student,
    get_current_active_user,
    require_admin,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["vacancies"],
)

# ══════════════════════════════════════════════════════
# Vacancy Management (Admin)
# ══════════════════════════════════════════════════════


@router.post(
    "/vacancies",
    response_model=VacancyResponse,
    status_code=HTTPStatus.CREATED,
    summary="Buat lowongan baru",
)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    session=Depends(get_session),
    current_user: DomainUser = Depends(require_admin),
) -> VacancyResponse:
    """
    Buat lowongan baru. Hanya admin yang bisa mengakses endpoint ini.
    """
    result = create_vacancy_command_handler(
        command=CreateVacancyCommand(
            payload=vacancy_data,
            created_by=current_user.id,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.vacancy


@router.get(
    "/vacancies",
    response_model=VacancyListResponse,
    summary="List semua lowongan aktif",
)
async def list_vacancies(
    page: int = Query(1, ge=1, description="Halaman"),
    per_page: int = Query(10, ge=1, le=100, description="Item per halaman"),
    is_active: bool = Query(True, description="Hanya lowongan aktif"),
    session=Depends(get_session),
    _: DomainUser = Depends(get_current_active_user),
) -> VacancyListResponse:
    """
    List semua lowongan aktif dengan pagination.
    """
    result = list_vacancies_command_handler(
        command=ListVacanciesCommand(
            page=page,
            per_page=per_page,
            is_active=is_active,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.data


@router.get(
    "/vacancies/search",
    response_model=VacancyListResponse,
    summary="Cari lowongan dengan filter",
)
async def search_vacancies(
    query: Optional[str] = Query(None, description="Kata kunci pencarian"),
    location: Optional[str] = Query(None, description="Filter lokasi"),
    type: Optional[VacancyType] = Query(None, alias="type", description="Tipe lowongan"),
    payment_type: Optional[PaymentType] = Query(None, alias="payment_type", description="Tipe pembayaran"),
    is_active: bool = Query(True, description="Hanya lowongan aktif"),
    page: int = Query(1, ge=1, description="Halaman"),
    per_page: int = Query(10, ge=1, le=100, description="Item per halaman"),
    session=Depends(get_session),
    _: DomainUser = Depends(get_current_active_user),
) -> VacancyListResponse:
    """
    Cari lowongan berdasarkan berbagai filter.
    """
    result = search_vacancies_command_handler(
        command=SearchVacanciesCommand(
            query=query,
            location=location,
            vacancy_type=type.value if type else None,
            payment_type=payment_type.value if payment_type else None,
            is_active=is_active,
            page=page,
            per_page=per_page,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.data


@router.get(
    "/vacancies/{vacancy_id}",
    response_model=VacancyDetailResponse,
    summary="Detail lowongan",
)
async def get_vacancy(
    vacancy_id: UUID,
    session=Depends(get_session),
    _: DomainUser = Depends(get_current_active_user),
) -> VacancyDetailResponse:
    """
    Ambil detail lowongan berdasarkan ID.
    """
    result = get_vacancy_command_handler(
        command=GetVacancyCommand(
            vacancy_id=vacancy_id,
            include_skills=True,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=result.error_message,
        )
    return result.vacancy


@router.put(
    "/vacancies/{vacancy_id}",
    response_model=VacancyResponse,
    summary="Update lowongan",
)
async def update_vacancy(
    vacancy_id: UUID,
    vacancy_data: VacancyUpdate,
    session=Depends(get_session),
    current_user: DomainUser = Depends(require_admin),
) -> VacancyResponse:
    """
    Update data lowongan. Hanya admin yang bisa mengakses endpoint ini.
    """
    result = update_vacancy_command_handler(
        command=UpdateVacancyCommand(
            vacancy_id=vacancy_id,
            payload=vacancy_data,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.vacancy


@router.delete(
    "/vacancies/{vacancy_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Hapus lowongan",
)
async def delete_vacancy(
    vacancy_id: UUID,
    session=Depends(get_session),
    current_user: DomainUser = Depends(require_admin),
) -> None:
    """
    Hapus lowongan (soft delete). Hanya admin yang bisa mengakses endpoint ini.
    """
    result = delete_vacancy_command_handler(
        command=DeleteVacancyCommand(vacancy_id=vacancy_id),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )


# ══════════════════════════════════════════════════════
# Wishlist (Student)
# ══════════════════════════════════════════════════════


@router.post(
    "/wishlist",
    response_model=WishlistResponse,
    status_code=HTTPStatus.CREATED,
    summary="Simpan lowongan ke wishlist",
)
async def add_wishlist(
    wishlist_data: WishlistCreate,
    session=Depends(get_session),
    current_student: DomainStudent = Depends(get_current_active_student),
) -> WishlistResponse:
    """
    Simpan lowongan ke wishlist student.
    """
    result = add_wishlist_command_handler(
        command=AddWishlistCommand(
            student_id=current_student.user_id,
            payload=wishlist_data,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.wishlist


@router.get(
    "/wishlist",
    response_model=WishlistListResponse,
    summary="List wishlist student",
)
async def list_wishlist(
    page: int = Query(1, ge=1, description="Halaman"),
    per_page: int = Query(10, ge=1, le=100, description="Item per halaman"),
    session=Depends(get_session),
    current_student: DomainStudent = Depends(get_current_active_student),
) -> WishlistListResponse:
    """
    List semua wishlist student.
    """
    result = list_wishlist_command_handler(
        command=ListWishlistCommand(
            student_id=current_student.user_id,
            page=page,
            per_page=per_page,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.data


@router.get(
    "/wishlist/{wishlist_id}",
    response_model=WishlistDetailResponse,
    summary="Detail wishlist",
)
async def get_wishlist(
    wishlist_id: UUID,
    session=Depends(get_session),
    current_student: DomainStudent = Depends(get_current_active_student),
) -> WishlistDetailResponse:
    """
    Ambil detail wishlist berdasarkan ID.
    """
    result = get_wishlist_command_handler(
        command=GetWishlistCommand(
            wishlist_id=wishlist_id,
            student_id=current_student.user_id,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=result.error_message,
        )
    return result.wishlist


@router.put(
    "/wishlist/{wishlist_id}",
    response_model=WishlistResponse,
    summary="Update catatan wishlist",
)
async def update_wishlist(
    wishlist_id: UUID,
    wishlist_data: WishlistUpdate,
    session=Depends(get_session),
    current_student: DomainStudent = Depends(get_current_active_student),
) -> WishlistResponse:
    """
    Update catatan pada wishlist.
    """
    result = update_wishlist_command_handler(
        command=UpdateWishlistCommand(
            wishlist_id=wishlist_id,
            student_id=current_student.user_id,
            payload=wishlist_data,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return result.wishlist


@router.delete(
    "/wishlist/{wishlist_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Hapus wishlist",
)
async def delete_wishlist(
    wishlist_id: UUID,
    session=Depends(get_session),
    current_student: DomainStudent = Depends(get_current_active_student),
) -> None:
    """
    Hapus lowongan dari wishlist.
    """
    result = delete_wishlist_command_handler(
        command=DeleteWishlistCommand(
            wishlist_id=wishlist_id,
            student_id=current_student.user_id,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
