"""
Login User Feature - Command Handler
Fitur untuk login dan autentikasi user
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app_backend.models.users import Users
from app_backend.schemas.user import UserLogin
from app_backend.shared.security import verify_password, create_access_token
from app_backend.domain.user import User as DomainUser


class LoginUserException(Exception):
    """Exception yang terjadi saat login user"""
    pass


@dataclass
class LoginUserCommand:
    """Command untuk login user"""
    payload: UserLogin


@dataclass
class LoginUserResult:
    """Result dari proses login"""
    access_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[DomainUser] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def login_user_command_handler(
    command: LoginUserCommand, 
    session: Session
) -> LoginUserResult:
    """
    Handle login user
    
    Business Rules:
    1. User harus ada dengan email yang diberikan
    2. Password harus cocok
    3. User harus aktif
    4. Generate JWT token jika autentikasi berhasil
    5. Update last_login_at
    """
    
    # Cari user berdasarkan email
    user = session.query(Users).filter(
        Users.email == command.payload.email
    ).first()
    
    if not user:
        return LoginUserResult(error_message="Email atau password salah")
    
    # Verifikasi password
    if not verify_password(command.payload.password, user.password_hash):
        return LoginUserResult(error_message="Email atau password salah")
    
    # Cek apakah user aktif
    if not user.is_active:
        return LoginUserResult(error_message="Akun dinonaktifkan")
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    session.commit()
    
    # Convert ke domain user
    domain_user = user.to_domain()
    
    # Buat access token
    token_data = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role
    }
    
    access_token = create_access_token(data=token_data)
    
    return LoginUserResult(
        access_token=access_token,
        token_type="bearer",
        user=domain_user
    )
