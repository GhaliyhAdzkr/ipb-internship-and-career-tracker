"""
Register Admin Feature – Command Handler.
Registrasi fasilitator/admin: buat auth.users + public.profiles_admin dalam satu transaksi.
Endpoint ini sebaiknya hanya dipanggil oleh super-admin yang sudah login,
atau dari internal script seeding.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.domain.user import UserRole
from app_backend.models.profiles_admin import ProfilesAdmin
from app_backend.models.users import Users
from app_backend.schemas.user import AdminRegister, UserResponse
from app_backend.shared.security import hash_password


class RegisterAdminException(Exception):
    pass


@dataclass
class RegisterAdminCommand:
    payload: AdminRegister


@dataclass
class RegisterAdminResult:
    user: Optional[UserResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def register_admin_command_handler(
    command: RegisterAdminCommand,
    session: Session,
) -> RegisterAdminResult:
    """
    Business Rules:
    1. Email harus unik (cek auth.users).
    2. NIP boleh None; jika diisi harus unik.
    3. Role di-hardcode ke ADMIN – tidak bisa diubah dari client.
    4. users dan profiles_admin dibuat dalam satu transaksi atomik.
    """
    if session.query(Users).filter(Users.email == command.payload.email).first():
        return RegisterAdminResult(error_message="Email sudah terdaftar")

    if command.payload.nip:
        if (
            session.query(ProfilesAdmin)
            .filter(ProfilesAdmin.nip == command.payload.nip)
            .first()
        ):
            return RegisterAdminResult(error_message="NIP sudah terdaftar")

    try:
        now = datetime.now(timezone.utc)
        user_id = uuid.uuid4()

        user = Users(
            id=user_id,
            email=command.payload.email,
            password_hash=hash_password(command.payload.password),
            role=UserRole.ADMIN.value,  # HARDCODED
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        profile = ProfilesAdmin(
            user_id=user_id,
            full_name=command.payload.full_name,
            unit_name=command.payload.unit_name,
            nip=command.payload.nip,
            updated_at=now,
        )

        session.add(user)
        session.flush()  # FK constraint: user harus ada sebelum profile
        session.add(profile)
        session.commit()
        session.refresh(user)

        return RegisterAdminResult(
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
        return RegisterAdminResult(error_message=str(exc))
    except Exception as exc:
        session.rollback()
        return RegisterAdminResult(error_message=f"Registrasi admin gagal: {exc}")
