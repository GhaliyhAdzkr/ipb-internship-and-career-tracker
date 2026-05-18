from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies
from app_backend.models.vacancies import Vacancies
from app_backend.schemas.wishlist import WishlistCreate, WishlistResponse


class AddWishlistException(Exception):
    pass


@dataclass
class AddWishlistCommand:
    student_id: uuid.UUID
    payload: WishlistCreate


@dataclass
class AddWishlistResult:
    wishlist: Optional[WishlistResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def add_wishlist_command_handler(
    command: AddWishlistCommand,
    session: Session,
) -> AddWishlistResult:
    """
    Business Rules:
    1. Vacancy harus ada dan aktif.
    2. Student tidak boleh duplikasi wishlist untuk vacancy yang sama.
    """
    # Check vacancy exists and is active
    vacancy = session.get(Vacancies, command.payload.vacancy_id)
    if not vacancy:
        return AddWishlistResult(error_message="Lowongan tidak ditemukan")

    if not vacancy.is_active:
        return AddWishlistResult(error_message="Lowongan sudah tidak aktif")

    # Check duplicate wishlist
    existing = (
        session.query(StudentWishlistVacancies)
        .filter(
            StudentWishlistVacancies.student_id == command.student_id,
            StudentWishlistVacancies.vacancy_id == command.payload.vacancy_id,
        )
        .first()
    )
    if existing:
        return AddWishlistResult(error_message="Lowongan sudah ada di wishlist")

    try:
        now = datetime.now(timezone.utc)

        wishlist = StudentWishlistVacancies(
            id=uuid.uuid4(),
            student_id=command.student_id,
            vacancy_id=command.payload.vacancy_id,
            notes=command.payload.notes,
            created_at=now,
        )

        session.add(wishlist)
        session.commit()
        session.refresh(wishlist)

        return AddWishlistResult(
            wishlist=WishlistResponse(
                id=wishlist.id,
                student_id=wishlist.student_id,
                vacancy_id=wishlist.vacancy_id,
                notes=wishlist.notes,
                created_at=wishlist.created_at,
            )
        )

    except Exception as exc:
        session.rollback()
        return AddWishlistResult(error_message=f"Gagal menyimpan ke wishlist: {exc}")
