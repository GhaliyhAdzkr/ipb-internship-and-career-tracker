"""
Auth Router - API endpoints untuk authentication
Berisi semua endpoint untuk registrasi, login, dan manajemen user
"""
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app_backend.features.auth.register_student import (
    RegisterStudentCommand,
    register_student_command_handler,
)
from app_backend.features.auth.register_company import (
    RegisterCompanyCommand,
    register_company_command_handler,
)
from app_backend.features.auth.register_lecturer import (
    RegisterLecturerCommand,
    register_lecturer_command_handler,
)
from app_backend.features.auth.login_user import (
    LoginUserCommand,
    login_user_command_handler,
)
from app_backend.features.auth.refresh_token import (
    RefreshTokenCommand,
    refresh_token_command_handler,
)
from app_backend.features.auth.reset_password import (
    RequestResetPasswordCommand,
    request_reset_password_command_handler,
    ResetPasswordCommand,
    reset_password_command_handler,
)
from app_backend.schemas.user import (
    StudentRegister, 
    CompanyRegister, 
    LecturerRegister,
    UserLogin, 
    UserResponse, 
    Token,
    TokenWithRefresh,
    RefreshTokenRequest,
    RequestResetPassword,
    ResetPassword
)
from app_backend.shared.database import get_session
from app_backend.shared.dependencies import get_current_user, get_current_active_user
from app_backend.domain.user import User as DomainUser

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["authentication"]
)


@router.post("/register/student", response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def register_student(
    student_data: StudentRegister,
    session=Depends(get_session),
) -> UserResponse:
    """
    Registrasi mahasiswa baru
    
    - **email**: Alamat email yang valid (harus unik)
    - **password**: Password (minimal 8 karakter, harus mengandung huruf besar, kecil, dan angka)
    - **nim**: Nomor Induk Mahasiswa (harus unik)
    - **full_name**: Nama lengkap mahasiswa
    - **semester**: Semester saat ini (1-14)
    
    Role otomatis diset ke STUDENT (tidak bisa diubah)
    """
    result = register_student_command_handler(
        command=RegisterStudentCommand(payload=student_data),
        session=session,
    )

    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, 
            detail=result.error_message
        )

    # Convert domain user ke response schema
    domain_user = result.user
    return UserResponse(
        id=domain_user.id,
        email=domain_user.email,
        role=domain_user.role,
        is_active=domain_user.is_active,
        last_login_at=domain_user.last_login_at,
        created_at=domain_user.created_at,
        updated_at=domain_user.updated_at
    )


@router.post("/register/company", response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def register_company(
    company_data: CompanyRegister,
    session=Depends(get_session),
) -> UserResponse:
    """
    Registrasi perusahaan baru
    
    - **email**: Alamat email yang valid (harus unik)
    - **password**: Password (minimal 8 karakter, harus mengandung huruf besar, kecil, dan angka)
    - **company_name**: Nama perusahaan
    - **industry**: Industri perusahaan (opsional)
    
    Role otomatis diset ke COMPANY (tidak bisa diubah)
    Akun perusahaan perlu verifikasi admin sebelum bisa posting lowongan
    """
    result = register_company_command_handler(
        command=RegisterCompanyCommand(payload=company_data),
        session=session,
    )

    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, 
            detail=result.error_message
        )

    # Convert domain user ke response schema
    domain_user = result.user
    return UserResponse(
        id=domain_user.id,
        email=domain_user.email,
        role=domain_user.role,
        is_active=domain_user.is_active,
        last_login_at=domain_user.last_login_at,
        created_at=domain_user.created_at,
        updated_at=domain_user.updated_at
    )


@router.post("/register/lecturer", response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def register_lecturer(
    lecturer_data: LecturerRegister,
    session=Depends(get_session),
) -> UserResponse:
    """
    Registrasi dosen baru
    
    - **email**: Alamat email yang valid (harus unik)
    - **password**: Password (minimal 8 karakter, harus mengandung huruf besar, kecil, dan angka)
    - **nip**: Nomor Induk Pegawai (harus unik)
    - **full_name**: Nama lengkap dosen
    - **department_id**: ID Departemen (opsional)
    
    Role otomatis diset ke LECTURER (tidak bisa diubah)
    """
    result = register_lecturer_command_handler(
        command=RegisterLecturerCommand(payload=lecturer_data),
        session=session,
    )

    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, 
            detail=result.error_message
        )

    # Convert domain user ke response schema
    domain_user = result.user
    return UserResponse(
        id=domain_user.id,
        email=domain_user.email,
        role=domain_user.role,
        is_active=domain_user.is_active,
        last_login_at=domain_user.last_login_at,
        created_at=domain_user.created_at,
        updated_at=domain_user.updated_at
    )


@router.post("/login", response_model=TokenWithRefresh)
async def login(
    credentials: UserLogin,
    session=Depends(get_session),
) -> TokenWithRefresh:
    """
    Login dengan email dan password
    
    Mengembalikan JWT access token dan refresh token jika autentikasi berhasil
    
    - **email**: Email user
    - **password**: Password user
    """
    result = login_user_command_handler(
        command=LoginUserCommand(payload=credentials),
        session=session,
    )

    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=result.error_message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert domain user ke response
    user_response = UserResponse(
        id=result.user.id,
        email=result.user.email,
        role=result.user.role,
        is_active=result.user.is_active,
        last_login_at=result.user.last_login_at,
        created_at=result.user.created_at,
        updated_at=result.user.updated_at
    )

    return TokenWithRefresh(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
        user=user_response
    )


@router.post("/refresh-token", response_model=TokenWithRefresh)
async def refresh_token(
    request: RefreshTokenRequest,
    session=Depends(get_session),
) -> TokenWithRefresh:
    """
    Refresh JWT access token menggunakan refresh token
    
    - **refresh_token**: Refresh token yang valid
    
    Mengembalikan access token baru dan refresh token baru
    """
    result = refresh_token_command_handler(
        command=RefreshTokenCommand(refresh_token=request.refresh_token),
        session=session,
    )

    if result.got_error():
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=result.error_message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert domain user ke response
    user_response = UserResponse(
        id=result.user.id,
        email=result.user.email,
        role=result.user.role,
        is_active=result.user.is_active,
        last_login_at=result.user.last_login_at,
        created_at=result.user.created_at,
        updated_at=result.user.updated_at
    )

    return TokenWithRefresh(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
        user=user_response
    )


@router.post("/password/reset-request", status_code=HTTPStatus.OK)
async def request_password_reset(
    request: RequestResetPassword,
    session=Depends(get_session),
) -> dict:
    """
    Meminta reset password dengan mengirim token reset ke email
    
    - **email**: Email user yang ingin reset password
    
    Catatan: 
    - Email sending belum aktif (perlu setup SMTP)
    """
    result = request_reset_password_command_handler(
        command=RequestResetPasswordCommand(payload=request),
        session=session,
    )

    # Selalu return sukses untuk mencegah email enumeration
    # Error handling tetap dilakukan di dalam command handler
    return {
        "message": "Jika email terdaftar, link reset password akan dikirim",
        "reset_password_token": result.token if result.token else None  # DEV ONLY: hapus di production
    }


@router.post("/password/reset", status_code=HTTPStatus.OK)
async def reset_password(
    request: ResetPassword,
    session=Depends(get_session),
) -> dict:
    """
    Reset password menggunakan token yang valid
    
    - **token**: Token reset password dari endpoint /password/reset-request
    - **new_password**: Password baru (minimal 8 karakter)
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

    return {"message": "Password berhasil direset"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: DomainUser = Depends(get_current_active_user)
) -> UserResponse:
    """
    Mendapatkan informasi user yang sedang login
    
    Memerlukan JWT token yang valid di Authorization header
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
        last_login_at=current_user.last_login_at,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.post("/logout", status_code=HTTPStatus.NO_CONTENT)
async def logout(
    current_user: DomainUser = Depends(get_current_user)
):
    """
    Logout user yang sedang login
    
    Catatan: Karena menggunakan JWT tokens, logout sebenarnya dilakukan di client-side
    dengan menghapus token. Endpoint ini ada untuk konsistensi API.
    Jika perlu server-side token blacklisting, implementasikan di sini.
    """
    # Dalam sistem JWT stateless, logout biasanya ditangani client-side
    # Jika butuh token blacklisting di server-side, implementasikan di sini
    return None
