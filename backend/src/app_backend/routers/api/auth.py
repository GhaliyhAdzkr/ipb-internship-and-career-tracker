"""
Auth Router – API endpoints untuk authentication & session management.

Endpoints:
  POST /register/student    – Registrasi mahasiswa
  POST /register/admin      – Registrasi admin/fasilitator (protected: admin only)
  POST /login               – Login, kembalikan access + refresh token
  POST /refresh-token       – Token rotation (stateful)
  POST /logout              – Revoke refresh token (device logout)
  POST /password/reset-request – Minta link reset password via email
  POST /password/reset         – Reset password dengan action token
  GET  /me                     – Info user yang sedang login
"""

from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File

from app_backend.conf.settings import settings
from app_backend.domain.user import User as DomainUser
from app_backend.features.auth.auth_service import AuthService
from app_backend.features.auth.logout import LogoutCommand, logout_command_handler
from app_backend.features.auth.refresh_token import RefreshTokenCommand, refresh_token_command_handler
from app_backend.features.auth.reset_password import (
    RequestResetPasswordCommand,
    ResetPasswordCommand,
    request_reset_password_command_handler,
    reset_password_command_handler,
)
from app_backend.schemas.user import (
    AdminRegister,
    LoginResponse,
    LogoutRequest,
    ProfileUpdate,
    RefreshTokenRequest,
    RequestResetPassword,
    ResetPassword,
    StudentRegister,
    UserLogin,
    UserResponse,
)
from app_backend.shared.auth_dependencies import get_current_active_user, require_admin
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import get_auth_service
from app_backend.shared.s3_storage import get_s3_client, upload_fileobj

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["authentication"],
)

# Registration


@router.get(
    "/register/check-availability",
    summary="Periksa ketersediaan email atau username",
)
async def check_availability(
    identifier: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Periksa ketersediaan email atau username secara asinkron (untuk as-you-type validation).
    Mendukung debouncing, caching performa tinggi Redis (SRE pattern), dan B-Tree lookup.
    """
    if not identifier or len(identifier) < 3:
        return {"available": False, "reason": "Identifier minimal 3 karakter"}

    # Optional: If email is input, validate domain as well
    if "@" in identifier:
        domain = identifier.split("@")[-1].lower()
        if domain not in ("ipb.ac.id", "apps.ipb.ac.id"):
            return {"available": False, "reason": "Domain email harus @ipb.ac.id atau @apps.ipb.ac.id"}

    result = auth_service.check_availability(identifier)
    return result


@router.post(
    "/register/student",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    summary="Registrasi mahasiswa baru",
)
async def register_student(
    student_data: StudentRegister,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """
    Daftarkan mahasiswa baru. Role otomatis **STUDENT**.

    - **email**: Alamat email unik
    - **password**: Min 8 char, harus ada angka + huruf besar + kecil
    - **nim**: NIM unik (6–20 karakter)
    - **full_name**: Nama lengkap
    - **semester**: Semester aktif (1–14)
    """
    try:
        return auth_service.register_student(student_data)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Registrasi gagal: {exc}",
        )


@router.post(
    "/register/admin",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    summary="Registrasi admin / fasilitator",
)
async def register_admin(
    admin_data: AdminRegister,
    auth_service: AuthService = Depends(get_auth_service),
    _: DomainUser = Depends(require_admin),  # hanya ADMIN yang bisa buat admin baru
) -> UserResponse:
    """
    Daftarkan fasilitator/admin baru. Role otomatis **ADMIN**.
    Endpoint ini hanya dapat dipanggil oleh admin yang sudah login.

    - **email**: Alamat email unik
    - **password**: Min 8 char, harus ada angka + huruf besar + kecil
    - **full_name**: Nama lengkap
    - **unit_name**: Unit kerja (contoh: CDA IPB)
    - **nip**: NIP (opsional, harus unik jika diisi)
    """
    try:
        return auth_service.register_admin(admin_data)
    except ValueError as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Registrasi gagal: {exc}",
        )


# Session management


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login – dapatkan access + refresh token",
)
async def login(
    credentials: UserLogin,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """
    Autentikasi email + password.
    Mengembalikan **access token** (stateless JWT) + **refresh token** (disimpan di DB).
    """
    ip_address: Optional[str] = request.client.host if request.client else None
    user_agent: Optional[str] = request.headers.get("user-agent")

    try:
        return auth_service.login(credentials, user_agent, ip_address)
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Login gagal: {exc}",
        )


@router.post(
    "/refresh-token",
    response_model=LoginResponse,
    summary="Rotate refresh token – terbitkan token baru",
)
async def refresh_token(
    request_body: RefreshTokenRequest,
    request: Request,
    session=Depends(get_session),
) -> LoginResponse:
    """
    Token rotation: validasi refresh token di DB, revoke yang lama,
    dan terbitkan access token + refresh token baru.
    """
    ip_address: Optional[str] = request.client.host if request.client else None
    user_agent: Optional[str] = request.headers.get("user-agent")

    result = refresh_token_command_handler(
        command=RefreshTokenCommand(
            payload=request_body,
            device_info=user_agent,
            ip_address=ip_address,
        ),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=result.error_message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result.data


@router.post(
    "/logout",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Logout – revoke refresh token sesi ini",
)
async def logout(
    request_body: LogoutRequest,
    session=Depends(get_session),
) -> None:
    """
    Revoke refresh token yang diberikan (device logout).
    Bersifat idempotent: logout ganda tidak menyebabkan error.
    """
    logout_command_handler(
        command=LogoutCommand(payload=request_body),
        session=session,
    )


# Password reset


@router.post(
    "/password/reset-request",
    status_code=HTTPStatus.OK,
    summary="Minta link reset password",
)
async def request_password_reset(
    request: RequestResetPassword,
    session=Depends(get_session),
) -> dict:
    """
    Kirim token reset password ke email terdaftar.
    Selalu mengembalikan respons generik untuk mencegah email enumeration.

    > **DEV**: Field `reset_token` hanya dikembalikan di mode development.
    > Di production, token dikirim via email dan tidak ada di response.
    """
    result = request_reset_password_command_handler(
        command=RequestResetPasswordCommand(payload=request),
        session=session,
    )
    response: dict = {"message": result.message}

    # Hanya kembalikan token di development mode
    if settings.is_development and result.token:
        response["reset_token"] = result.token

    return response


@router.post(
    "/password/reset",
    status_code=HTTPStatus.OK,
    summary="Reset password dengan action token",
)
async def reset_password(
    request: ResetPassword,
    session=Depends(get_session),
) -> dict:
    """
    Reset password menggunakan token yang diterima dari email.
    Token bersifat one-time use dan akan dinonaktifkan setelah dipakai.
    """
    result = reset_password_command_handler(
        command=ResetPasswordCommand(payload=request),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return {"message": result.message}


@router.post(
    "/verify-email",
    status_code=HTTPStatus.OK,
    summary="Verifikasi email mahasiswa",
)
async def verify_email(
    token: str,
    session=Depends(get_session),
) -> dict:
    """
    Aktivasi akun mahasiswa menggunakan token yang dikirim melalui email saat registrasi.
    """
    from app_backend.features.auth.verify_email import VerifyEmailCommand, verify_email_command_handler

    result = verify_email_command_handler(
        command=VerifyEmailCommand(token=token),
        session=session,
    )
    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.error_message,
        )
    return {"message": result.message}


# Current user info


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Info user yang sedang login",
)
async def get_me(
    current_user: DomainUser = Depends(get_current_active_user),
    session=Depends(get_session),
) -> UserResponse:
    """Kembalikan data profil user berdasarkan JWT access token."""
    from app_backend.models.profiles_student import ProfilesStudent
    from app_backend.models.profiles_admin import ProfilesAdmin

    full_name = None
    nim = None
    semester = None
    unit_name = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    cv_url: Optional[str] = None
    avatar_url: Optional[str] = None
    gpa = None
    department_id = None
    department_name = None

    if current_user.role == "STUDENT":
        profile = session.query(ProfilesStudent).filter(ProfilesStudent.user_id == current_user.id).first()
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
    elif current_user.role == "ADMIN":
        profile = session.query(ProfilesAdmin).filter(ProfilesAdmin.user_id == current_user.id).first()
        if profile:
            full_name = profile.full_name
            unit_name = profile.unit_name

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
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
        last_login_at=current_user.last_login_at,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.put(
    "/profile",
    response_model=UserResponse,
    summary="Update data profil user",
)
async def update_profile(
    payload: ProfileUpdate,
    current_user: DomainUser = Depends(get_current_active_user),
    session=Depends(get_session),
) -> UserResponse:
    """Update data di tabel profil (student/admin)."""
    from app_backend.models.profiles_student import ProfilesStudent
    from app_backend.models.profiles_admin import ProfilesAdmin
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)

    if current_user.role == "STUDENT":
        profile = session.query(ProfilesStudent).filter(ProfilesStudent.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profil mahasiswa tidak ditemukan")

        if payload.full_name:
            profile.full_name = payload.full_name
        if payload.semester:
            profile.semester = payload.semester
        if payload.nim:
            profile.nim = payload.nim
        if payload.phone_number:
            profile.phone_number = payload.phone_number
        if payload.linkedin_url:
            profile.linkedin_url = payload.linkedin_url
        if payload.gpa is not None:
            profile.gpa = payload.gpa
        if payload.department_id:
            profile.department_id = payload.department_id

        profile.updated_at = now

    elif current_user.role == "ADMIN":
        profile = session.query(ProfilesAdmin).filter(ProfilesAdmin.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profil admin tidak ditemukan")

        if payload.full_name:
            profile.full_name = payload.full_name

        profile.updated_at = now

    session.commit()
    return await get_me(current_user=current_user, session=session)


@router.post(
    "/profile/avatar",
    response_model=UserResponse,
    summary="Upload foto profil",
)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: DomainUser = Depends(get_current_active_user),
    session=Depends(get_session),
) -> UserResponse:
    """Upload dan ganti foto profil user."""
    from app_backend.models.profiles_student import ProfilesStudent
    from app_backend.models.profiles_admin import ProfilesAdmin

    # Validasi Tipe File
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Hanya file gambar yang diizinkan")

    # Path File di S3 (Disesuaikan dengan Policy Supabase: folder pertama harus 'public')
    ext = file.filename.split(".")[-1]
    file_key = f"public/avatars/{current_user.id}.{ext}"

    # Upload ke S3
    s3_client = get_s3_client()
    success = upload_fileobj(
        client=s3_client, fileobj=file.file, bucket=settings.s3_bucket, key=file_key, content_type=file.content_type
    )

    if not success:
        raise HTTPException(status_code=500, detail="Gagal mengunggah foto ke storage")

    # URL Public Supabase (Gunakan format public object URL)
    base_url = settings.s3_endpoint.replace(".storage.supabase.co/storage/v1/s3", ".supabase.co/storage/v1/object/public")
    avatar_url = f"{base_url}/{settings.s3_bucket}/{file_key}"

    # Update Database
    if current_user.role == "STUDENT":
        profile = session.query(ProfilesStudent).filter(ProfilesStudent.user_id == current_user.id).first()
        if profile:
            profile.avatar_url = avatar_url
    elif current_user.role == "ADMIN":
        profile = session.query(ProfilesAdmin).filter(ProfilesAdmin.user_id == current_user.id).first()
        if profile:
            profile.avatar_url = avatar_url

    session.commit()
    return await get_me(current_user=current_user, session=session)


@router.get(
    "/departments",
    summary="List master departemen",
)
async def get_departments(
    session=Depends(get_session),
):
    """Ambil daftar departemen untuk lookup profil."""
    from app_backend.models.master_departments import MasterDepartments

    departments = session.query(MasterDepartments).all()
    return [{"id": d.id, "name": d.name, "faculty": d.faculty} for d in departments]
