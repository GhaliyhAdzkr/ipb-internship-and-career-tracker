"""
Logout Feature
Revoke refresh token satu sesi tertentu (device logout).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.schemas.user import LogoutRequest
from app_backend.shared.security import hash_token


@dataclass
class LogoutCommand:
    payload: LogoutRequest


@dataclass
class LogoutResult:
    success: bool = False
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def logout_command_handler(
    command: LogoutCommand,
    session: Session,
) -> LogoutResult:
    """
    Business Rules:
    1. Cari refresh token di DB berdasarkan hash.
    2. Jika tidak ditemukan atau sudah di-revoke → kembalikan sukses
       (idempotent: logout ganda tidak menyebabkan error).
    3. Tandai is_revoked = true.
    """
    token_hash = hash_token(command.payload.refresh_token)

    db_token = (
        session.query(UserRefreshTokens)
        .filter(UserRefreshTokens.token_hash == token_hash)
        .first()
    )

    if db_token and not db_token.is_revoked:
        db_token.revoke()
        session.commit()

    return LogoutResult(success=True)
