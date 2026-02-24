"""
Domain Models Package
Pure business logic models tanpa dependency ke infrastructure
"""

from app_backend.domain.application import Application, ApplicationStatus
from app_backend.domain.company import Company
from app_backend.domain.placement import Placement, PlacementStatus
from app_backend.domain.student import Student
from app_backend.domain.user import User, UserRole
from app_backend.domain.vacancy import Vacancy, VacancyType

__all__ = [
    # User
    "User",
    "UserRole",
    # Student
    "Student",
    # Company
    "Company",
    # Vacancy
    "Vacancy",
    "VacancyType",
    # Application
    "Application",
    "ApplicationStatus",
    # Placement
    "Placement",
    "PlacementStatus",
]
