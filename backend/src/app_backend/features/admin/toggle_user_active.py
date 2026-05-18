from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.users import Users
from app_backend.schemas.user import UserResponse


@dataclass
class ToggleUserActiveCommand:
    user_id: uuid.UUID


@dataclass
class ToggleUserActiveResult:
    user: Optional[UserResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def toggle_user_active_command_handler(
    command: ToggleUserActiveCommand,
    session: Session,
) -> ToggleUserActiveResult:
    """
    Business Rules:
    1. User harus ada.
    2. Toggle is_active: True → False, False → True.
    3. Update updated_at.
    """
    user = session.query(Users).filter(Users.id == command.user_id).first()
    if not user:
        return ToggleUserActiveResult(error_message="User tidak ditemukan")

    user.is_active = not user.is_active
    user.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(user)

    return ToggleUserActiveResult(
        user=UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    )
