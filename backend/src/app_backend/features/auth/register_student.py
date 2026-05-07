"""
Register Student Feature – Command Handler.
Registrasi mahasiswa: buat auth.users + public.profiles_student dalam satu transaksi.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.domain.user import UserRole
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.users import Users
from app_backend.schemas.user import StudentRegister, UserResponse
from app_backend.shared.security import hash_password


class RegisterStudentException(Exception):
    pass


@dataclass
class RegisterStudentCommand:
    payload: StudentRegister


@dataclass
class RegisterStudentResult:
    user: Optional[UserResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def register_student_command_handler(
    command: RegisterStudentCommand,
    session: Session,
) -> RegisterStudentResult:
    """
    Business Rules:
    1. Email harus unik (cek auth.users).
    2. NIM harus unik (cek profiles_student).
    3. Role di-hardcode ke STUDENT – tidak bisa diubah dari client.
    4. user dan profile_student dibuat dalam satu transaksi atomik.
    """
    if session.query(Users).filter(Users.email == command.payload.email).first():
        return RegisterStudentResult(error_message="Email sudah terdaftar")

    if session.query(ProfilesStudent).filter(ProfilesStudent.nim == command.payload.nim).first():
        return RegisterStudentResult(error_message="NIM sudah terdaftar")

    try:
        now = datetime.now(timezone.utc)
        user_id = uuid.uuid4()

        user = Users(
            id=user_id,
            email=command.payload.email,
            password_hash=hash_password(command.payload.password),
            role=UserRole.STUDENT.value,  # HARDCODED – tidak bisa dari client
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        profile = ProfilesStudent(
            user_id=user_id,
            nim=command.payload.nim,
            full_name=command.payload.full_name,
            semester=command.payload.semester,
            is_mbkm_eligible=True,
            updated_at=now,
        )

        session.add(user)
        session.flush()  # FK constraint: user harus ada sebelum profile
        session.add(profile)
        session.commit()
        session.refresh(user)

        return RegisterStudentResult(
            user=UserResponse(
                id=user.id,
                email=user.email,
                role=user.role,
                is_active=user.is_active if user.is_active is not None else True,
                last_login_at=user.last_login_at,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        )

    except ValueError as exc:
        session.rollback()
        return RegisterStudentResult(error_message=str(exc))
    except Exception as exc:
        session.rollback()
        return RegisterStudentResult(error_message=f"Registrasi gagal: {exc}")
