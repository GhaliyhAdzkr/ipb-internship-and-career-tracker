"""
Register Student Feature - Command Handler
Fitur untuk registrasi mahasiswa baru
"""
import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app_backend.domain.user import User as DomainUser, UserRole
from app_backend.domain.student import Student as DomainStudent
from app_backend.models.users import Users
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.schemas.user import StudentRegister
from app_backend.shared.security import hash_password


class RegisterStudentException(Exception):
    """Exception yang terjadi saat registrasi mahasiswa"""
    pass


@dataclass
class RegisterStudentCommand:
    """Command untuk registrasi mahasiswa baru"""
    payload: StudentRegister


@dataclass
class RegisterStudentResult:
    """Result dari proses registrasi mahasiswa"""
    user: Optional[DomainUser] = None
    student: Optional[DomainStudent] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def register_student_command_handler(
    command: RegisterStudentCommand, 
    session: Session
) -> RegisterStudentResult:
    """
    Handle registrasi mahasiswa baru
    
    Business Rules:
    1. Email harus unik
    2. NIM harus unik
    3. Password harus di-hash sebelum disimpan
    4. Role otomatis STUDENT (tidak bisa diubah dari client)
    5. User dan profile student dibuat bersamaan dalam transaksi
    """
    
    # Cek apakah email sudah ada
    existing_email = session.query(Users).filter(
        Users.email == command.payload.email
    ).first()
    
    if existing_email:
        return RegisterStudentResult(error_message="Email sudah terdaftar")
    
    # Cek apakah NIM sudah ada
    existing_nim = session.query(ProfilesStudent).filter(
        ProfilesStudent.nim == command.payload.nim
    ).first()
    
    if existing_nim:
        return RegisterStudentResult(error_message="NIM sudah terdaftar")
    
    try:
        # Generate user ID
        user_id = uuid.uuid4()
        
        # Buat domain user (ROLE HARDCODED KE STUDENT)
        domain_user = DomainUser(
            id=user_id,
            email=command.payload.email,
            password_hash=hash_password(command.payload.password),
            role=UserRole.STUDENT.value,  # HARDCODED - tidak dari input user
            is_active=True,
            last_login_at=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Buat domain student
        domain_student = DomainStudent(
            user_id=user_id,
            nim=command.payload.nim,
            full_name=command.payload.full_name,
            semester=command.payload.semester,
            department_id=None,
            gpa=None,
            is_mbkm_eligible=False,
            updated_at=datetime.utcnow()
        )
        
        # Convert ke ORM models
        user_model = Users.from_domain(domain_user)
        student_model = ProfilesStudent(
            user_id=domain_student.user_id,
            nim=domain_student.nim,
            full_name=domain_student.full_name,
            semester=domain_student.semester,
            department_id=domain_student.department_id,
            gpa=domain_student.gpa,
            is_mbkm_eligible=domain_student.is_mbkm_eligible,
            updated_at=domain_student.updated_at
        )
        
        # Simpan dalam transaksi
        session.add(user_model)
        session.add(student_model)
        session.commit()
        session.refresh(user_model)
        session.refresh(student_model)
        
        # Return domain models
        return RegisterStudentResult(
            user=user_model.to_domain(),
            student=domain_student
        )
        
    except ValueError as e:
        # Error validasi domain
        session.rollback()
        return RegisterStudentResult(error_message=str(e))
    except Exception as e:
        session.rollback()
        return RegisterStudentResult(error_message=f"Registrasi gagal: {str(e)}")
