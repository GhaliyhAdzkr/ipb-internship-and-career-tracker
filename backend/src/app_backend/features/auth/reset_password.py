"""
Reset Password Feature – Command Handlers.
Menggunakan auth.auth_action_tokens (stateful, one-time token) bukan JWT
agar token bisa di-invalidate secara eksplisit dan dicegah re-use.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.conf.settings import settings
from app_backend.models.auth_action_tokens import AuthActionTokens
from app_backend.models.users import Users
from app_backend.schemas.user import RequestResetPassword, ResetPassword
from app_backend.shared.security import (generate_secure_token, hash_password,
                                         hash_token)

# ============ Request Reset Password ============


@dataclass
class RequestResetPasswordCommand:
    payload: RequestResetPassword


@dataclass
class RequestResetPasswordResult:
    """
    `token` hanya diisi di mode DEV untuk testing via API.
    Di production, kirim via email dan hapus field ini dari response.
    """

    token: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def request_reset_password_command_handler(
    command: RequestResetPasswordCommand,
    session: Session,
) -> RequestResetPasswordResult:
    """
    Business Rules:
    1. Selalu kembalikan pesan sukses generik (mencegah email enumeration).
    2. Jika email terdaftar & aktif: buat AuthActionToken baru dengan
       action_type=RESET_PASSWORD dan simpan hash ke DB.
    3. Kirim raw token via email (stub: kembalikan di response untuk dev).
    """
    GENERIC_MSG = (
        "Jika email terdaftar, instruksi reset password akan dikirim ke email Anda"
    )

    user = session.query(Users).filter(Users.email == command.payload.email).first()

    if not user or not user.is_active:
        return RequestResetPasswordResult(message=GENERIC_MSG)

    raw_token = generate_secure_token()
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.reset_password_token_expire_minutes
    )

    action_token = AuthActionTokens(
        user_id=user.id,
        token_hash=hash_token(raw_token),
        action_type="RESET_PASSWORD",
        expires_at=expires_at,
        is_used=False,
    )
    session.add(action_token)
    session.commit()

    # TODO: Kirim raw_token via email (SMTP worker).
    # Di production: hapus field `token` dari response ini.
    return RequestResetPasswordResult(
        token=raw_token,  # DEV ONLY
        message=GENERIC_MSG,
    )


# ============ Reset Password ============


@dataclass
class ResetPasswordCommand:
    payload: ResetPassword


@dataclass
class ResetPasswordResult:
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def reset_password_command_handler(
    command: ResetPasswordCommand,
    session: Session,
) -> ResetPasswordResult:
    """
    Business Rules:
    1. Cari token di DB berdasarkan hash (SHA-256).
    2. Token harus belum dipakai dan belum expired.
    3. Hash password baru, update auth.users, tandai token as used.
    """
    token_hash = hash_token(command.payload.token)

    action_token = (
        session.query(AuthActionTokens)
        .filter(
            AuthActionTokens.token_hash == token_hash,
            AuthActionTokens.action_type == "RESET_PASSWORD",
        )
        .first()
    )

    if not action_token or not action_token.is_valid():
        return ResetPasswordResult(error_message="Token tidak valid atau sudah expired")

    user = session.query(Users).filter(Users.id == action_token.user_id).first()
    if not user or not user.is_active:
        return ResetPasswordResult(
            error_message="User tidak ditemukan atau tidak aktif"
        )

    try:
        user.password_hash = hash_password(command.payload.new_password)
        user.updated_at = datetime.now(timezone.utc)
        action_token.mark_used()
        session.commit()
        return ResetPasswordResult(message="Password berhasil direset")
    except Exception as exc:
        session.rollback()
        return ResetPasswordResult(error_message=f"Reset password gagal: {exc}")
