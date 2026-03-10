"""
Delete Vacancy Feature – Command Handler.
Menghapus lowongan (soft delete via is_active=False).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.vacancies import Vacancies


class DeleteVacancyException(Exception):
    pass


@dataclass
class DeleteVacancyCommand:
    vacancy_id: uuid.UUID


@dataclass
class DeleteVacancyResult:
    success: bool = False
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def delete_vacancy_command_handler(
    command: DeleteVacancyCommand,
    session: Session,
) -> DeleteVacancyResult:
    """
    Soft delete vacancy by setting is_active=False.
    """
    vacancy = session.get(Vacancies, command.vacancy_id)

    if not vacancy:
        return DeleteVacancyResult(error_message="Lowongan tidak ditemukan")

    try:
        # Soft delete - just set inactive
        vacancy.is_active = False
        session.commit()

        return DeleteVacancyResult(success=True)

    except Exception as exc:
        session.rollback()
        return DeleteVacancyResult(error_message=f"Gagal menghapus lowongan: {exc}")
