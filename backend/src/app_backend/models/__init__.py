"""
Models package – re-exports semua ORM entity dari file atomik.

Import order penting: Base harus diimport pertama agar semua model
teregistrasi ke metadata yang sama sebelum digunakan.
"""

from app_backend.models.activity_logs import ActivityLogs  # noqa: F401
from app_backend.models.application_logs import ApplicationLogs  # noqa: F401
# --- Public schema: applications ---
from app_backend.models.applications import Applications  # noqa: F401
from app_backend.models.auth_action_tokens import \
    AuthActionTokens  # noqa: F401
# --- Shared base ---
from app_backend.models.base import Base  # noqa: F401
# --- Public schema: documents & notifications ---
from app_backend.models.document_requests import DocumentRequests  # noqa: F401
# --- Public schema: master data ---
from app_backend.models.master_departments import \
    MasterDepartments  # noqa: F401
from app_backend.models.master_external_companies import \
    MasterExternalCompanies  # noqa: F401
from app_backend.models.master_skills import MasterSkills  # noqa: F401
from app_backend.models.notification_queue import \
    NotificationQueue  # noqa: F401
# --- Public schema: placements & activity ---
from app_backend.models.placements import Placements  # noqa: F401
# --- Public schema: profiles ---
from app_backend.models.profiles_admin import ProfilesAdmin  # noqa: F401
from app_backend.models.profiles_student import ProfilesStudent  # noqa: F401
# --- Public schema: skills junction ---
from app_backend.models.student_skills import StudentSkills  # noqa: F401
from app_backend.models.student_wishlist_vacancies import \
    StudentWishlistVacancies  # noqa: F401
from app_backend.models.user_refresh_tokens import \
    UserRefreshTokens  # noqa: F401
# --- Auth schema ---
from app_backend.models.users import Users  # noqa: F401
# --- Public schema: vacancies ---
from app_backend.models.vacancies import Vacancies  # noqa: F401
from app_backend.models.vacancy_skills import VacancySkills  # noqa: F401
# --- Views ---
from app_backend.models.views import \
    t_view_internship_distribution  # noqa: F401

__all__ = [
    "Base",
    # auth
    "Users",
    "UserRefreshTokens",
    "AuthActionTokens",
    # master
    "MasterDepartments",
    "MasterExternalCompanies",
    "MasterSkills",
    # profiles
    "ProfilesAdmin",
    "ProfilesStudent",
    # skills
    "StudentSkills",
    "VacancySkills",
    # vacancies
    "Vacancies",
    "StudentWishlistVacancies",
    # applications
    "Applications",
    "ApplicationLogs",
    # placements
    "Placements",
    "ActivityLogs",
    # documents & notifications
    "DocumentRequests",
    "NotificationQueue",
    # views
    "t_view_internship_distribution",
]
