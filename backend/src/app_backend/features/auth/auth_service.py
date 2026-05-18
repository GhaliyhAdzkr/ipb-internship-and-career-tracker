import uuid
from datetime import datetime, timedelta, timezone
from typing import Protocol

from app_backend.conf.settings import settings
from app_backend.domain.user import UserRole
from app_backend.models.auth_action_tokens import AuthActionTokens
from app_backend.models.profiles_admin import ProfilesAdmin
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.models.users import Users
from app_backend.repositories.admin_repository import AdminRepository
from app_backend.repositories.refresh_token_repository import RefreshTokenRepository
from app_backend.repositories.student_repository import StudentRepository
from app_backend.repositories.user_repository import UserRepository
from app_backend.schemas.user import AdminRegister, LoginResponse, StudentRegister, UserLogin, UserResponse
from app_backend.shared.mailer import send_direct_email
from app_backend.shared.cache import cache_get, cache_set, cache_delete
from app_backend.shared.security import (
    create_access_token,
    create_refresh_token,
    generate_secure_token,
    hash_password,
    hash_token,
    verify_password,
)


class IAuthService(Protocol):
    def register_student(self, data: StudentRegister) -> UserResponse: ...
    def register_admin(self, data: AdminRegister) -> UserResponse: ...
    def login(self, data: UserLogin, device_info: str = None, ip_address: str = None) -> LoginResponse: ...


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

            base_username = data.email.split("@")[0]
            username = base_username
            suffix = 1
            from sqlalchemy import select

            while self.user_repo.session.scalars(select(Users).where(Users.username == username)).first():
                username = f"{base_username}{suffix}"
                suffix += 1

            user = Users(
                id=user_id,
                email=data.email,
                username=username,
                password_hash=hash_password(data.password),
                role=UserRole.STUDENT.value,
                is_active=False,  # AKUN TIDAK AKTIF SAMPAI DIVERIFIKASI
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

            # Invalidate availability cache keys
            cache_delete(f"availability:identifier:{data.email.lower()}")
            cache_delete(f"availability:identifier:{username.lower()}")

            # Buat Token Verifikasi
            raw_token = generate_secure_token()
            expires_at = now + timedelta(hours=24)

            verification_token = AuthActionTokens(
                user_id=user_id,
                token_hash=hash_token(raw_token),
                action_type="ACTIVATE_ACCOUNT",
                expires_at=expires_at,
                is_used=False,
            )
            self.user_repo.session.add(verification_token)
            self.user_repo.save_changes()

            verification_link = f"{settings.frontend_url}/verify-email?token={raw_token}"
            subject = "Your LARAS verification link"
            body = f"""
A new registration attempt was made to create a LARAS account for <strong>{user.email}</strong>.
<br><br>
Was this you? Please click the verification button below to activate your account:
<br><br>
<div class="btn-container">
    <a href="{verification_link}" class="btn-action">
       Verify My Account
    </a>
</div>
<br>
Or copy and paste the following URL into your browser:
<div class="raw-link">
    <a href="{verification_link}">{verification_link}</a>
</div>
<br>
This verification link is valid for 24 hours. If you did not make this request, please ignore this email.
"""
            import threading

            threading.Thread(
                target=send_direct_email, args=(user.email, subject, body), kwargs={"user_name": data.full_name}, daemon=True
            ).start()

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

            base_username = data.email.split("@")[0]
            username = base_username
            suffix = 1
            from sqlalchemy import select

            while self.user_repo.session.scalars(select(Users).where(Users.username == username)).first():
                username = f"{base_username}{suffix}"
                suffix += 1

            user = Users(
                id=user_id,
                email=data.email,
                username=username,
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

            # Invalidate availability cache keys
            cache_delete(f"availability:identifier:{data.email.lower()}")
            cache_delete(f"availability:identifier:{username.lower()}")

            self.user_repo.save_changes()
            return self._map_user_to_response(user)
        except Exception as exc:
            self.user_repo.rollback()
            raise exc

    def login(self, data: UserLogin, device_info: str = None, ip_address: str = None) -> LoginResponse:
        if "@" in data.email:
            user = self.user_repo.get_by_email(data.email)
        else:
            from sqlalchemy import select, or_, and_

            query = select(Users).where(
                or_(Users.username == data.email, and_(Users.username.is_(None), Users.email.like(data.email + "@%")))
            )
            users = self.user_repo.session.scalars(query).all()
            if not users:
                user = None
            elif len(users) == 1:
                user = users[0]
            else:
                user = None
                for u in users:
                    if verify_password(data.password, u.password_hash):
                        user = u
                        break
                if not user:
                    user = users[0]

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
        full_name = None
        nim = None
        semester = None
        unit_name = None
        phone_number = None
        linkedin_url = None
        cv_url = None
        avatar_url = None
        gpa = None
        department_id = None
        department_name = None

        if user.role == "STUDENT":
            profile = self.student_repo.get_by_user_id(user.id)
            if profile:
                full_name = profile.full_name
                nim = profile.nim
                semester = profile.semester
                phone_number = profile.phone_number
                linkedin_url = profile.linkedin_url
                cv_url = profile.cv_url
                avatar_url = profile.avatar_url
                gpa = float(profile.gpa) if profile.gpa else None
                department_id = profile.department_id
                if profile.department:
                    department_name = profile.department.name
        elif user.role == "ADMIN":
            profile = self.admin_repo.get_by_user_id(user.id)
            if profile:
                full_name = profile.full_name
                unit_name = profile.unit_name
                avatar_url = profile.avatar_url

        return UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active if user.is_active is not None else True,
            full_name=full_name,
            nim=nim,
            semester=semester,
            unit_name=unit_name,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            cv_url=cv_url,
            avatar_url=avatar_url,
            gpa=gpa,
            department_id=department_id,
            department_name=department_name,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def check_availability(self, identifier: str) -> dict:
        """
        Check if an email or username is already taken.
        Applies Redis caching for O(1) cache hits (Google SRE pattern) with B-Tree database fallback.
        """
        clean_identifier = identifier.strip().lower()
        cache_key = f"availability:identifier:{clean_identifier}"

        # 1. Try Cache Hit
        cached = cache_get(cache_key)
        if cached is not None:
            return {"available": cached == "available", "source": "cache"}

        # 2. Database B-Tree Index Range Lookup
        from sqlalchemy import select, or_, and_

        if "@" in clean_identifier:
            query = select(Users).where(Users.email == clean_identifier)
        else:
            query = select(Users).where(
                or_(Users.username == clean_identifier, and_(Users.username.is_(None), Users.email.like(clean_identifier + "@%")))
            )

        exists_user = self.user_repo.session.scalars(query).first()
        is_available = exists_user is None

        # 3. Cache the result for future lookup (expires in 10 minutes to maintain consistency)
        status = "available" if is_available else "taken"
        cache_set(cache_key, status, ttl=600)

        return {"available": is_available, "source": "db"}
