"""
Login User Feature – Command Handler.
Autentikasi email+password, catat refresh token stateful ke DB.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.conf.settings import settings
from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.models.users import Users
from app_backend.schemas.user import LoginResponse, UserLogin, UserResponse
from app_backend.shared.security import create_access_token, create_refresh_token, hash_token, verify_password


class LoginUserException(Exception):
    pass


@dataclass
class LoginUserCommand:
    payload: UserLogin
    device_info: Optional[str] = None
    ip_address: Optional[str] = None


@dataclass
class LoginUserResult:
    data: Optional[LoginResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def login_user_command_handler(
    command: LoginUserCommand,
    session: Session,
) -> LoginUserResult:
    """
    Business Rules:
    1. Email harus terdaftar dan password cocok.
    2. Akun harus aktif (is_active = true).
    3. Buat access token (stateless JWT) + refresh token (stateful di DB).
    4. Catat last_login_at.
    """
    user = session.query(Users).filter(Users.email == command.payload.email).first()

    # Selalu kembalikan pesan generik untuk mencegah user enumeration
    if not user or not verify_password(command.payload.password, user.password_hash):
        return LoginUserResult(error_message="Email atau password salah")

    if not user.is_active:
        return LoginUserResult(error_message="Akun dinonaktifkan. Hubungi admin.")

    token_payload = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
    }

    access_token = create_access_token(data=token_payload)
    raw_refresh_token = create_refresh_token(data={"user_id": str(user.id)})

    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    db_refresh = UserRefreshTokens(
        user_id=user.id,
        token_hash=hash_token(raw_refresh_token),
        device_info=command.device_info,
        ip_address=command.ip_address,
        expires_at=expires_at,
        is_revoked=False,
    )
    session.add(db_refresh)

    user.last_login_at = datetime.now(timezone.utc)
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

    return LoginUserResult(
        data=LoginResponse(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=user_response,
        )
    )
