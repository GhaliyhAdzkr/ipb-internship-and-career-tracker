"""
Import all ORM models
"""
# Master tables
from app_backend.models.master_departments import MasterDepartments
from app_backend.models.master_skills import MasterSkills

# Users
from app_backend.models.users import Users

# Notification Queue
from app_backend.models.notification_queue import NotificationQueue

# Profiles
from app_backend.models.profiles_company import ProfilesCompany
from app_backend.models.profiles_lecturer import ProfilesLecturer
from app_backend.models.profiles_student import ProfilesStudent

# Skills relation tables
from app_backend.models.student_skills import StudentSkills

# Document Requests
from app_backend.models.document_requests import DocumentRequests

# Vacancies
from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills

# Applications
from app_backend.models.applications import Applications
from app_backend.models.application_logs import ApplicationLogs

# Placements
from app_backend.models.placements import Placements
from app_backend.models.activity_logs import ActivityLogs
from app_backend.models.placement_milestones import PlacementMilestones
from app_backend.models.sks_conversions import SksConversions

__all__ = [
    # Master tables
    "MasterDepartments",
    "MasterSkills",
    # Users
    "Users",
    # Notification Queue
    "NotificationQueue",
    # Profiles
    "ProfilesCompany",
    "ProfilesLecturer",
    "ProfilesStudent",
    # Skills
    "StudentSkills",
    # Documents
    "DocumentRequests",
    # Vacancies
    "Vacancies",
    "VacancySkills",
    # Applications
    "Applications",
    "ApplicationLogs",
    # Placements
    "Placements",
    "ActivityLogs",
    "PlacementMilestones",
    "SksConversions",
]
