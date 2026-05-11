from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app_backend.models.auth_action_tokens import AuthActionTokens
from app_backend.models.users import Users
from app_backend.shared.security import hash_token


@dataclass
class VerifyEmailCommand:
    token: str


@dataclass
class VerifyEmailResult:
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def verify_email_command_handler(
    command: VerifyEmailCommand,
    session: Session,
) -> VerifyEmailResult:
    """
    Business Rules:
    1. Cari token ACTIVATE_ACCOUNT di DB.
    2. Pastikan belum expired dan belum digunakan.
    3. Aktifkan user (is_active = True).
    4. Tandai token as used.
    """
    token_hash = hash_token(command.token)

    action_token = (
        session.query(AuthActionTokens)
        .filter(
            AuthActionTokens.token_hash == token_hash,
            AuthActionTokens.action_type == "ACTIVATE_ACCOUNT",
        )
        .first()
    )

    if not action_token:
        return VerifyEmailResult(error_message="Token verifikasi tidak ditemukan")

    user = session.query(Users).filter(Users.id == action_token.user_id).first()
    if not user:
        return VerifyEmailResult(error_message="User tidak ditemukan")

    # Idempotensi: Jika user sudah aktif, anggap sukses meskipun token sudah ditandai used
    if user.is_active:
        if not action_token.is_used:
            action_token.mark_used()
            session.commit()
        return VerifyEmailResult(message="Email sudah terverifikasi sebelumnya. Akun Anda sudah aktif.")

    if not action_token.is_valid():
        return VerifyEmailResult(error_message="Token verifikasi sudah expired atau telah digunakan")

    try:
        user.is_active = True
        user.updated_at = datetime.now(timezone.utc)
        action_token.mark_used()
        session.commit()
        return VerifyEmailResult(message="Email berhasil diverifikasi. Akun Anda kini aktif.")
    except Exception as exc:
        session.rollback()
        return VerifyEmailResult(error_message=f"Verifikasi gagal: {exc}")
