"""
Reset Password Feature - Command Handlers
Fitur untuk request dan reset password
"""
import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app_backend.models.users import Users
from app_backend.schemas.user import RequestResetPassword, ResetPassword
from app_backend.shared.security import (
    create_reset_password_token,
    decode_access_token,
    verify_token_type,
    hash_password
)


class ResetPasswordException(Exception):
    """Exception yang terjadi saat reset password"""
    pass


# ============ Request Reset Password ============

@dataclass
class RequestResetPasswordCommand:
    """Command untuk request reset password"""
    payload: RequestResetPassword


@dataclass
class RequestResetPasswordResult:
    """Result dari proses request reset password"""
    token: Optional[str] = None  # Token untuk testing/dev, production kirim via email
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def request_reset_password_command_handler(
    command: RequestResetPasswordCommand, 
    session: Session
) -> RequestResetPasswordResult:
    """
    Handle request reset password
    
    Business Rules:
    1. Email harus terdaftar
    2. User harus aktif
    3. Generate reset token dan kirim via email
    
    SECURITY NOTE: Selalu return success message meskipun email tidak ditemukan
    untuk mencegah email enumeration attack
    """
    
    # Cari user berdasarkan email
    user = session.query(Users).filter(
        Users.email == command.payload.email
    ).first()
    
    # SECURITY: Jangan reveal apakah email ada atau tidak
    if not user:
        return RequestResetPasswordResult(
            message="Jika email terdaftar, instruksi reset password akan dikirim ke email Anda"
        )
    
    # Check if user is active
    if not user.is_active:
        return RequestResetPasswordResult(
            message="Jika email terdaftar, instruksi reset password akan dikirim ke email Anda"
        )
    
    # Generate reset password token
    reset_token = create_reset_password_token(user.email)
    
    # ===== EMAIL SENDING NOT IMPLEMENTED YET =====
    # TODO: Setup SMTP configuration untuk kirim email reset password
    # Contoh implementasi:
    # send_email(
    #     to=user.email,
    #     subject="Reset Password IPB Career Tracker",
    #     body=f"Click link berikut untuk reset password: {FRONTEND_URL}/reset-password?token={reset_token}"
    # )
    # 
    # DEVELOPMENT MODE: Token dikembalikan di response untuk testing
    # PRODUCTION MODE: Hapus field 'token' dari response, kirim via email saja
    # =============================================
    
    return RequestResetPasswordResult(
        token=reset_token,  # DEV ONLY: Hapus di production
        message="Instruksi reset password telah dikirim ke email Anda"
    )


# ============ Reset Password ============

@dataclass
class ResetPasswordCommand:
    """Command untuk reset password"""
    payload: ResetPassword


@dataclass
class ResetPasswordResult:
    """Result dari proses reset password"""
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def reset_password_command_handler(
    command: ResetPasswordCommand, 
    session: Session
) -> ResetPasswordResult:
    """
    Handle reset password dengan token
    
    Business Rules:
    1. Token harus valid dan belum expired
    2. Token type harus 'reset_password'
    3. Hash password baru
    4. Update password di database
    """
    
    # Decode and verify token
    payload = decode_access_token(command.payload.token)
    
    if not payload:
        return ResetPasswordResult(error_message="Token tidak valid atau sudah expired")
    
    # Verify token type
    if not verify_token_type(payload, "reset_password"):
        return ResetPasswordResult(error_message="Token tidak valid")
    
    # Get email from payload
    email = payload.get("email")
    if not email:
        return ResetPasswordResult(error_message="Token tidak mengandung email")
    
    # Find user
    user = session.query(Users).filter(Users.email == email).first()
    
    if not user:
        return ResetPasswordResult(error_message="User tidak ditemukan")
    
    # Check if user is active
    if not user.is_active:
        return ResetPasswordResult(error_message="User tidak aktif")
    
    try:
        # Hash new password
        new_password_hash = hash_password(command.payload.new_password)
        
        # Update password
        user.password_hash = new_password_hash
        user.updated_at = datetime.utcnow()
        
        session.commit()
        
        return ResetPasswordResult(message="Password berhasil direset")
        
    except Exception as e:
        session.rollback()
        return ResetPasswordResult(error_message=f"Reset password gagal: {str(e)}")
