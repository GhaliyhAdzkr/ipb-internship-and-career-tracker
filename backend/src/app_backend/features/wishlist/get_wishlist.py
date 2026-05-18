from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies
from app_backend.models.vacancies import Vacancies
from app_backend.schemas.wishlist import WishlistDetailResponse, WishlistSummary


class GetWishlistException(Exception):
    pass


@dataclass
class GetWishlistCommand:
    wishlist_id: uuid.UUID
    student_id: uuid.UUID


@dataclass
class GetWishlistResult:
    wishlist: Optional[WishlistDetailResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def get_wishlist_command_handler(
    command: GetWishlistCommand,
    session: Session,
) -> GetWishlistResult:
    """
    Ambil detail wishlist dengan info vacancy.
    """
    wishlist = (
        session.query(StudentWishlistVacancies)
        .options(joinedload(StudentWishlistVacancies.vacancy).joinedload(Vacancies.company))
        .filter(StudentWishlistVacancies.id == command.wishlist_id)
        .first()
    )

    if not wishlist:
        return GetWishlistResult(error_message="Wishlist tidak ditemukan")

    if wishlist.student_id != command.student_id:
        return GetWishlistResult(error_message="Tidak berhak melihat wishlist ini")

    vacancy = wishlist.vacancy

    vacancy_summary = WishlistSummary(
        id=vacancy.id,
        title=vacancy.title,
        location=vacancy.location,
        type=vacancy.type,
        payment_type=vacancy.payment_type,
        open_date=vacancy.open_date,
        close_date=vacancy.close_date,
    )

    return GetWishlistResult(
        wishlist=WishlistDetailResponse(
            id=wishlist.id,
            student_id=wishlist.student_id,
            vacancy=vacancy_summary,
            notes=wishlist.notes,
            created_at=wishlist.created_at,
        )
    )
