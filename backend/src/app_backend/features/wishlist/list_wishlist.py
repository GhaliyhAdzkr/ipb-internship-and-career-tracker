"""
List Wishlist Feature – Command Handler.
Mengambil semua wishlist student.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app_backend.models.student_wishlist_vacancies import StudentWishlistVacancies
from app_backend.models.vacancies import Vacancies
from app_backend.schemas.wishlist import (
    WishlistDetailResponse,
    WishlistListResponse,
    WishlistSummary,
)


class ListWishlistException(Exception):
    pass


@dataclass
class ListWishlistCommand:
    student_id: uuid.UUID
    page: int = 1
    per_page: int = 10


@dataclass
class ListWishlistResult:
    data: Optional[WishlistListResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_wishlist_command_handler(
    command: ListWishlistCommand,
    session: Session,
) -> ListWishlistResult:
    """
    List semua wishlist student dengan pagination.
    """
    page = max(1, command.page)
    per_page = min(max(1, command.per_page), 100)
    offset = (page - 1) * per_page

    # Base query
    query = (
        session.query(StudentWishlistVacancies)
        .options(
            joinedload(StudentWishlistVacancies.vacancy)
            .joinedload(Vacancies.company)
        )
        .filter(StudentWishlistVacancies.student_id == command.student_id)
    )

    # Get total count
    total = query.count()

    # Get paginated results
    wishlists = query.order_by(StudentWishlistVacancies.created_at.desc()).offset(offset).limit(per_page).all()

    # Build response
    items = []
    for wishlist in wishlists:
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

        items.append(
            WishlistDetailResponse(
                id=wishlist.id,
                student_id=wishlist.student_id,
                vacancy=vacancy_summary,
                notes=wishlist.notes,
                created_at=wishlist.created_at,
            )
        )

    return ListWishlistResult(
        data=WishlistListResponse(
            items=items,
            total=total,
        )
    )
