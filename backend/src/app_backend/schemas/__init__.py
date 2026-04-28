"""
Pydantic schemas package – re-exports semua schema untuk convenience.
"""

# Admin schemas
from app_backend.schemas.admin import AdminProfileResponse  # noqa: F401
from app_backend.schemas.admin import (AdminProfileUpdate, CompanyCreate,
                                       CompanyResponse, CompanyUpdate,
                                       DepartmentCreate, DepartmentResponse,
                                       DepartmentUpdate, SkillCreate,
                                       SkillResponse, SkillUpdate)
# Profile schemas
from app_backend.schemas.profile import CVDataUpdate  # noqa: F401
from app_backend.schemas.profile import (DepartmentInfo, SkillInfo,
                                         SkillUpdate, StudentProfileResponse)
# Auth schemas
from app_backend.schemas.user import AdminRegister  # noqa: F401
from app_backend.schemas.user import (ChangePassword, LoginResponse,
                                      LogoutRequest, RefreshTokenRequest,
                                      RequestResetPassword, ResetPassword,
                                      StudentRegister, Token, TokenData,
                                      TokenWithRefresh, UserLogin,
                                      UserResponse, UserRole)
# Vacancy schemas
from app_backend.schemas.vacancy import VacancyCreate  # noqa: F401
from app_backend.schemas.vacancy import (VacancyDetailResponse,
                                         VacancyListResponse, VacancyResponse,
                                         VacancyUpdate)
# Wishlist schemas
from app_backend.schemas.wishlist import WishlistCreate  # noqa: F401
from app_backend.schemas.wishlist import (WishlistDetailResponse,
                                          WishlistListResponse,
                                          WishlistResponse, WishlistUpdate)
