"""
Delete Wishlist Feature – Command Handler.
Menghapus vacancy dari wishlist student.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.student_wishlist_vacancies import \
    StudentWishlistVacancies


class DeleteWishlistException(Exception):
    pass


@dataclass
class DeleteWishlistCommand:
    wishlist_id: uuid.UUID
    student_id: uuid.UUID


@dataclass
class DeleteWishlistResult:
    success: bool = False
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def delete_wishlist_command_handler(
    command: DeleteWishlistCommand,
    session: Session,
) -> DeleteWishlistResult:
    """
    Hapus wishlist student.
    """
    wishlist = session.get(StudentWishlistVacancies, command.wishlist_id)

    if not wishlist:
        return DeleteWishlistResult(error_message="Wishlist tidak ditemukan")

    if wishlist.student_id != command.student_id:
        return DeleteWishlistResult(error_message="Tidak berhak menghapus wishlist ini")

    try:
        session.delete(wishlist)
        session.commit()

        return DeleteWishlistResult(success=True)

    except Exception as exc:
        session.rollback()
        return DeleteWishlistResult(error_message=f"Gagal menghapus wishlist: {exc}")
