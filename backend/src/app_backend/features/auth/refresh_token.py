"""
Refresh Token Feature – Command Handler.
Token rotation: validasi refresh token di DB, terbitkan access + refresh baru,
dan revoke refresh token lama (per-device session management).
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.conf.settings import settings
from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.models.users import Users
from app_backend.schemas.user import LoginResponse, RefreshTokenRequest, UserResponse
from app_backend.shared.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_token,
    verify_token_type,
)


class RefreshTokenException(Exception):
    pass


@dataclass
class RefreshTokenCommand:
    payload: RefreshTokenRequest
    device_info: Optional[str] = None
    ip_address: Optional[str] = None


@dataclass
class RefreshTokenResult:
    data: Optional[LoginResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def refresh_token_command_handler(
    command: RefreshTokenCommand,
    session: Session,
) -> RefreshTokenResult:
    """
    Business Rules (Token Rotation):
    1. JWT signature + expiry harus valid.
    2. Token type harus 'refresh'.
    3. DB record harus ada, belum di-revoke, dan belum expired.
    4. User masih aktif.
    5. Revoke token lama, terbitkan token baru (rotation).
    """
    raw_token = command.payload.refresh_token

    # 1. Decode JWT
    payload = decode_access_token(raw_token)
    if not payload or not verify_token_type(payload, "refresh"):
        return RefreshTokenResult(error_message="Refresh token tidak valid")

    user_id_str = payload.get("user_id")
    try:
        user_id = uuid.UUID(user_id_str)
    except (TypeError, ValueError):
        return RefreshTokenResult(error_message="Refresh token tidak valid")

    # 2. Cek di DB
    token_hash = hash_token(raw_token)
    db_token = session.query(UserRefreshTokens).filter(UserRefreshTokens.token_hash == token_hash).first()

    if not db_token or not db_token.is_valid():
        return RefreshTokenResult(error_message="Refresh token tidak valid atau sudah di-revoke")

    # 3. Cek user
    user = session.query(Users).filter(Users.id == user_id).first()
    if not user or not user.is_active:
        return RefreshTokenResult(error_message="User tidak ditemukan atau tidak aktif")

    # 4. Revoke token lama
    db_token.revoke()

    # 5. Terbitkan token baru
    new_access_token = create_access_token(data={"user_id": str(user.id), "email": user.email, "role": user.role})
    new_raw_refresh = create_refresh_token(data={"user_id": str(user.id)})

    new_db_token = UserRefreshTokens(
        user_id=user.id,
        token_hash=hash_token(new_raw_refresh),
        device_info=command.device_info or db_token.device_info,
        ip_address=command.ip_address or db_token.ip_address,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days),
        is_revoked=False,
    )
    session.add(new_db_token)
    session.commit()

    user_response = UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active if user.is_active is not None else True,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    return RefreshTokenResult(
        data=LoginResponse(
            access_token=new_access_token,
            refresh_token=new_raw_refresh,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=user_response,
        )
    )
