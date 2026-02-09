"""
Refresh Token Feature - Command Handler
Fitur untuk refresh JWT access token
"""
import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.users import Users
from app_backend.schemas.user import RefreshTokenRequest
from app_backend.shared.security import (
    decode_access_token, 
    verify_token_type,
    create_access_token,
    create_refresh_token
)
from app_backend.domain.user import User as DomainUser


class RefreshTokenException(Exception):
    """Exception yang terjadi saat refresh token"""
    pass


@dataclass
class RefreshTokenCommand:
    """Command untuk refresh token"""
    payload: RefreshTokenRequest


@dataclass
class RefreshTokenResult:
    """Result dari proses refresh token"""
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[DomainUser] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def refresh_token_command_handler(
    command: RefreshTokenCommand, 
    session: Session
) -> RefreshTokenResult:
    """
    Handle refresh JWT token
    
    Business Rules:
    1. Refresh token harus valid
    2. Token type harus 'refresh'
    3. User masih aktif
    4. Generate new access token dan refresh token
    """
    
    # Decode refresh token
    payload = decode_access_token(command.payload.refresh_token)
    
    if not payload:
        return RefreshTokenResult(error_message="Refresh token tidak valid")
    
    # Verify token type
    if not verify_token_type(payload, "refresh"):
        return RefreshTokenResult(error_message="Token type tidak valid")
    
    # Get user_id from payload
    user_id_str = payload.get("user_id")
    if not user_id_str:
        return RefreshTokenResult(error_message="Token tidak mengandung user_id")
    
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        return RefreshTokenResult(error_message="User ID tidak valid")
    
    # Get user from database
    user = session.query(Users).filter(Users.id == user_id).first()
    
    if not user:
        return RefreshTokenResult(error_message="User tidak ditemukan")
    
    # Check if user is active
    if not user.is_active:
        return RefreshTokenResult(error_message="User tidak aktif")
    
    # Convert to domain user
    domain_user = user.to_domain()
    
    # Create new access token
    access_token_data = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role
    }
    new_access_token = create_access_token(data=access_token_data)
    
    # Create new refresh token
    refresh_token_data = {
        "user_id": str(user.id)
    }
    new_refresh_token = create_refresh_token(data=refresh_token_data)
    
    return RefreshTokenResult(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        user=domain_user
    )
