"""
Pydantic schemas package – re-exports semua schema untuk convenience.
"""

# Admin schemas
from app_backend.schemas.admin import AdminProfileResponse  # noqa: F401
# Profile schemas
from app_backend.schemas.profile import CVDataUpdate  # noqa: F401
# Auth schemas
from app_backend.schemas.user import AdminRegister  # noqa: F401
# Vacancy schemas
from app_backend.schemas.vacancy import VacancyCreate  # noqa: F401
# Wishlist schemas
from app_backend.schemas.wishlist import WishlistCreate  # noqa: F401
