from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies
from app_backend.schemas.wishlist import WishlistResponse, WishlistUpdate


class UpdateWishlistException(Exception):
    pass


@dataclass
class UpdateWishlistCommand:
    wishlist_id: uuid.UUID
    student_id: uuid.UUID
    payload: WishlistUpdate


@dataclass
class UpdateWishlistResult:
    wishlist: Optional[WishlistResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def update_wishlist_command_handler(
    command: UpdateWishlistCommand,
    session: Session,
) -> UpdateWishlistResult:
    """
    Update notes pada wishlist.
    """
    wishlist = session.get(StudentWishlistVacancies, command.wishlist_id)

    if not wishlist:
        return UpdateWishlistResult(error_message="Wishlist tidak ditemukan")

    if wishlist.student_id != command.student_id:
        return UpdateWishlistResult(error_message="Tidak berhak mengubah wishlist ini")

    try:
        if command.payload.notes is not None:
            wishlist.notes = command.payload.notes

        session.commit()
        session.refresh(wishlist)

        return UpdateWishlistResult(
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
        return UpdateWishlistResult(error_message=f"Gagal mengupdate wishlist: {exc}")
