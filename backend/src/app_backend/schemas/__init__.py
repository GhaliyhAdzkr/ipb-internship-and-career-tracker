"""
Pydantic schemas package – re-exports semua schema untuk convenience.
"""

# Auth schemas
from app_backend.schemas.user import (  # noqa: F401
    AdminRegister,
    ChangePassword,
    LoginResponse,
    LogoutRequest,
    RefreshTokenRequest,
    RequestResetPassword,
    ResetPassword,
    StudentRegister,
    Token,
    TokenData,
    TokenWithRefresh,
    UserLogin,
    UserResponse,
    UserRole,
)

# Profile schemas
from app_backend.schemas.profile import (  # noqa: F401
    CVDataUpdate,
    DepartmentInfo,
    SkillInfo,
    SkillUpdate,
    StudentProfileResponse,
)

# Admin schemas
from app_backend.schemas.admin import (  # noqa: F401
    AdminProfileResponse,
    AdminProfileUpdate,
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)

# Vacancy schemas
from app_backend.schemas.vacancy import (  # noqa: F401
    VacancyCreate,
    VacancyDetailResponse,
    VacancyListResponse,
    VacancyResponse,
    VacancyUpdate,
)

# Wishlist schemas
from app_backend.schemas.wishlist import (  # noqa: F401
    WishlistCreate,
    WishlistDetailResponse,
    WishlistListResponse,
    WishlistResponse,
    WishlistUpdate,
)
