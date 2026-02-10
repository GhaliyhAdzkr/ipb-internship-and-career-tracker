"""
Register Lecturer Feature - Command Handler
Fitur untuk registrasi dosen baru
"""
import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app_backend.domain.user import User as DomainUser, UserRole
from app_backend.models.users import Users
from app_backend.models.profiles_lecturer import ProfilesLecturer
from app_backend.schemas.user import LecturerRegister
from app_backend.shared.security import hash_password


class RegisterLecturerException(Exception):
    """Exception yang terjadi saat registrasi dosen"""
    pass


@dataclass
class RegisterLecturerCommand:
    """Command untuk registrasi dosen baru"""
    payload: LecturerRegister


@dataclass
class RegisterLecturerResult:
    """Result dari proses registrasi dosen"""
    user: Optional[DomainUser] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def register_lecturer_command_handler(
    command: RegisterLecturerCommand, 
    session: Session
) -> RegisterLecturerResult:
    """
    Handle registrasi dosen baru
    
    Business Rules:
    1. Email harus unik
    2. NIP harus unik
    3. Password harus di-hash sebelum disimpan
    4. Role otomatis LECTURER (tidak bisa diubah dari client)
    5. User dan profile lecturer dibuat bersamaan dalam transaksi
    """
    
    # Cek apakah email sudah ada
    existing_email = session.query(Users).filter(
        Users.email == command.payload.email
    ).first()
    
    if existing_email:
        return RegisterLecturerResult(error_message="Email sudah terdaftar")
    
    # Cek apakah NIP sudah ada
    existing_nip = session.query(ProfilesLecturer).filter(
        ProfilesLecturer.nip == command.payload.nip
    ).first()
    
    if existing_nip:
        return RegisterLecturerResult(error_message="NIP sudah terdaftar")
    
    try:
        # Generate user ID
        user_id = uuid.uuid4()
        
        # Buat domain user (ROLE HARDCODED KE LECTURER)
        domain_user = DomainUser(
            id=user_id,
            email=command.payload.email,
            password_hash=hash_password(command.payload.password),
            role=UserRole.LECTURER.value,  # HARDCODED - tidak dari input user
            is_active=True,
            last_login_at=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Convert ke ORM models
        user_model = Users.from_domain(domain_user)
        lecturer_model = ProfilesLecturer(
            user_id=user_id,
            nip=command.payload.nip,
            full_name=command.payload.full_name,
            department_id=command.payload.department_id,
            max_mentoring_slots=10,  # Default value
            updated_at=datetime.utcnow()
        )
        
        # Simpan dalam transaksi - PENTING: flush user dulu sebelum add profile
        session.add(user_model)
        session.flush()  # Pastikan user ter-insert dulu ke database
        session.add(lecturer_model)
        session.commit()
        session.refresh(user_model)
        session.refresh(lecturer_model)
        
        # Return domain model
        return RegisterLecturerResult(user=user_model.to_domain())
        
    except ValueError as e:
        # Error validasi domain
        session.rollback()
        return RegisterLecturerResult(error_message=str(e))
    except Exception as e:
        session.rollback()
        return RegisterLecturerResult(error_message=f"Registrasi gagal: {str(e)}")
