"""
Security utilities untuk password hashing dan JWT tokens
Berisi fungsi untuk hash password dan generate JWT token
"""
from datetime import datetime, timedelta
from typing import Optional
import uuid
import bcrypt

from jose import JWTError, jwt

from app_backend.conf.settings import settings


def hash_password(password: str) -> str:
    """Hash sebuah password menggunakan bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password terhadap hash-nya
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True jika password cocok, False jika tidak
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Buat JWT access token
    
    Args:
        data: Data yang akan di-encode ke dalam token
        expires_delta: Custom expire time
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    
    # Convert UUID ke string untuk JSON serialization
    if "user_id" in to_encode and isinstance(to_encode["user_id"], uuid.UUID):
        to_encode["user_id"] = str(to_encode["user_id"])
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Buat JWT refresh token dengan expire time lebih lama
    
    Args:
        data: Data minimal yang akan di-encode (biasanya hanya user_id)
        
    Returns:
        JWT refresh token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    # Convert UUID ke string
    if "user_id" in to_encode and isinstance(to_encode["user_id"], uuid.UUID):
        to_encode["user_id"] = str(to_encode["user_id"])
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_reset_password_token(email: str) -> str:
    """Buat token untuk reset password
    
    Args:
        email: Email user yang request reset password
        
    Returns:
        JWT token string
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.reset_password_token_expire_minutes)
    
    to_encode = {
        "email": email,
        "exp": expire,
        "type": "reset_password"
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode dan verify JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload atau None jika invalid
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def verify_token_type(payload: dict, expected_type: str) -> bool:
    """Verify bahwa token memiliki tipe yang benar
    
    Args:
        payload: Decoded JWT payload
        expected_type: Expected token type (access, refresh, reset_password)
        
    Returns:
        True jika tipe cocok, False jika tidak
    """
    return payload.get("type") == expected_type
