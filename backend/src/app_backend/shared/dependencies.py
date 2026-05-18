from fastapi import Depends
from sqlalchemy.orm import Session

from app_backend.features.admin.master_data_service import MasterDataService
from app_backend.features.application.application_service import ApplicationService
from app_backend.features.auth.auth_service import AuthService
from app_backend.features.placement.placement_service import PlacementService
from app_backend.features.profile.profile_service import ProfileService
from app_backend.features.vacancy.vacancy_service import VacancyService
from app_backend.repositories.activity_log_repository import ActivityLogRepository
from app_backend.repositories.admin_repository import AdminRepository
from app_backend.repositories.application_log_repository import ApplicationLogRepository
from app_backend.repositories.application_repository import ApplicationRepository
from app_backend.repositories.company_repository import CompanyRepository
from app_backend.repositories.department_repository import DepartmentRepository
from app_backend.repositories.placement_repository import PlacementRepository
from app_backend.repositories.refresh_token_repository import RefreshTokenRepository
from app_backend.repositories.skill_repository import SkillRepository
from app_backend.repositories.student_repository import StudentRepository
from app_backend.repositories.student_skill_repository import StudentSkillRepository
from app_backend.repositories.user_repository import UserRepository
from app_backend.repositories.vacancy_repository import VacancyRepository
from app_backend.repositories.vacancy_skill_repository import VacancySkillRepository
from app_backend.shared.database import get_session


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_student_repository(
    session: Session = Depends(get_session),
) -> StudentRepository:
    return StudentRepository(session)


def get_admin_repository(session: Session = Depends(get_session)) -> AdminRepository:
    return AdminRepository(session)


def get_refresh_token_repository(
    session: Session = Depends(get_session),
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


def get_vacancy_repository(
    session: Session = Depends(get_session),
) -> VacancyRepository:
    return VacancyRepository(session)


def get_vacancy_skill_repository(
    session: Session = Depends(get_session),
) -> VacancySkillRepository:
    return VacancySkillRepository(session)


def get_company_repository(
    session: Session = Depends(get_session),
) -> CompanyRepository:
    return CompanyRepository(session)


def get_department_repository(
    session: Session = Depends(get_session),
) -> DepartmentRepository:
    return DepartmentRepository(session)


def get_skill_repository(session: Session = Depends(get_session)) -> SkillRepository:
    return SkillRepository(session)


def get_application_repository(
    session: Session = Depends(get_session),
) -> ApplicationRepository:
    return ApplicationRepository(session)


def get_application_log_repository(
    session: Session = Depends(get_session),
) -> ApplicationLogRepository:
    return ApplicationLogRepository(session)


def get_placement_repository(
    session: Session = Depends(get_session),
) -> PlacementRepository:
    return PlacementRepository(session)


def get_activity_log_repository(
    session: Session = Depends(get_session),
) -> ActivityLogRepository:
    return ActivityLogRepository(session)


def get_student_skill_repository(
    session: Session = Depends(get_session),
) -> StudentSkillRepository:
    return StudentSkillRepository(session)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    student_repo: StudentRepository = Depends(get_student_repository),
    admin_repo: AdminRepository = Depends(get_admin_repository),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repository),
) -> AuthService:
    return AuthService(user_repo, student_repo, admin_repo, refresh_token_repo)


def get_vacancy_service(
    vacancy_repo: VacancyRepository = Depends(get_vacancy_repository),
    vacancy_skill_repo: VacancySkillRepository = Depends(get_vacancy_skill_repository),
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> VacancyService:
    return VacancyService(vacancy_repo, vacancy_skill_repo, company_repo)


def get_master_data_service(
    department_repo: DepartmentRepository = Depends(get_department_repository),
    skill_repo: SkillRepository = Depends(get_skill_repository),
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> MasterDataService:
    return MasterDataService(department_repo, skill_repo, company_repo)


def get_application_service(
    application_repo: ApplicationRepository = Depends(get_application_repository),
    application_log_repo: ApplicationLogRepository = Depends(get_application_log_repository),
    student_repo: StudentRepository = Depends(get_student_repository),
    placement_repo: PlacementRepository = Depends(get_placement_repository),
) -> ApplicationService:
    return ApplicationService(application_repo, application_log_repo, student_repo, placement_repo)


def get_placement_service(
    placement_repo: PlacementRepository = Depends(get_placement_repository),
    activity_log_repo: ActivityLogRepository = Depends(get_activity_log_repository),
) -> PlacementService:
    return PlacementService(placement_repo, activity_log_repo)


def get_profile_service(
    student_repo: StudentRepository = Depends(get_student_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    student_skill_repo: StudentSkillRepository = Depends(get_student_skill_repository),
) -> ProfileService:
    return ProfileService(student_repo, user_repo, student_skill_repo)
