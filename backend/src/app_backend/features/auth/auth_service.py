import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Protocol

from sqlalchemy.orm import Session

from app_backend.conf.settings import settings
from app_backend.domain.user import UserRole
from app_backend.models.profiles_admin import ProfilesAdmin
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.models.users import Users
from app_backend.repositories.admin_repository import AdminRepository
from app_backend.repositories.refresh_token_repository import \
    RefreshTokenRepository
from app_backend.repositories.student_repository import StudentRepository
from app_backend.repositories.user_repository import UserRepository
from app_backend.schemas.user import (AdminRegister, LoginResponse,
                                      StudentRegister, UserLogin, UserResponse)
from app_backend.shared.security import (create_access_token,
                                         create_refresh_token, hash_password,
                                         hash_token, verify_password)


class IAuthService(Protocol):
    def register_student(self, data: StudentRegister) -> UserResponse: ...
    def register_admin(self, data: AdminRegister) -> UserResponse: ...
    def login(
        self, data: UserLogin, device_info: str = None, ip_address: str = None
    ) -> LoginResponse: ...


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        student_repo: StudentRepository,
        admin_repo: AdminRepository,
        refresh_token_repo: RefreshTokenRepository,
    ):
        self.user_repo = user_repo
        self.student_repo = student_repo
        self.admin_repo = admin_repo
        self.refresh_token_repo = refresh_token_repo

    def register_student(self, data: StudentRegister) -> UserResponse:
        if self.user_repo.get_by_email(data.email):
            raise ValueError("Email sudah terdaftar")
        if self.student_repo.get_by_nim(data.nim):
            raise ValueError("NIM sudah terdaftar")

        try:
            now = datetime.now(timezone.utc)
            user_id = uuid.uuid4()
            user = Users(
                id=user_id,
                email=data.email,
                password_hash=hash_password(data.password),
                role=UserRole.STUDENT.value,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            profile = ProfilesStudent(
                user_id=user_id,
                nim=data.nim,
                full_name=data.full_name,
                semester=data.semester,
                is_mbkm_eligible=True,
                updated_at=now,
            )
            self.user_repo.create(user)
            self.user_repo.flush()
            self.student_repo.create(profile)
            self.user_repo.save_changes()

            return self._map_user_to_response(user)
        except Exception as exc:
            self.user_repo.rollback()
            raise exc

    def register_admin(self, data: AdminRegister) -> UserResponse:
        if self.user_repo.get_by_email(data.email):
            raise ValueError("Email sudah terdaftar")
        if data.nip and self.admin_repo.get_by_nip(data.nip):
            raise ValueError("NIP sudah terdaftar")

        try:
            now = datetime.now(timezone.utc)
            user_id = uuid.uuid4()
            user = Users(
                id=user_id,
                email=data.email,
                password_hash=hash_password(data.password),
                role=UserRole.ADMIN.value,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            profile = ProfilesAdmin(
                user_id=user_id,
                nip=data.nip,
                full_name=data.full_name,
                unit_name=data.unit_name,
                updated_at=now,
            )
            self.user_repo.create(user)
            self.user_repo.flush()
            self.admin_repo.create(profile)
            self.user_repo.save_changes()
            return self._map_user_to_response(user)
        except Exception as exc:
            self.user_repo.rollback()
            raise exc

    def login(
        self, data: UserLogin, device_info: str = None, ip_address: str = None
    ) -> LoginResponse:
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise ValueError("Email atau password salah")

        if not user.is_active:
            raise PermissionError("Akun dinonaktifkan. Hubungi admin.")

        now = datetime.now(timezone.utc)
        token_payload = {
            "user_id": str(user.id),
            "email": user.email,
            "role": user.role,
        }
        access_token = create_access_token(data=token_payload)
        raw_refresh_token = create_refresh_token(data={"user_id": str(user.id)})

        expires_at = now + timedelta(days=settings.refresh_token_expire_days)
        db_refresh = UserRefreshTokens(
            user_id=user.id,
            token_hash=hash_token(raw_refresh_token),
            device_info=device_info,
            ip_address=ip_address,
            expires_at=expires_at,
            is_revoked=False,
        )
        self.refresh_token_repo.create(db_refresh)
        user.last_login_at = now
        self.user_repo.save_changes()

        return LoginResponse(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=self._map_user_to_response(user),
        )

    def _map_user_to_response(self, user: Users) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active if user.is_active is not None else True,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
