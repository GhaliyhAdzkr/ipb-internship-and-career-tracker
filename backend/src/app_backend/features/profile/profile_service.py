import uuid
from datetime import datetime, timezone
from typing import Optional, Protocol

from sqlalchemy.orm import joinedload, selectinload

from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.student_skills import StudentSkills
from app_backend.repositories.student_repository import StudentRepository
from app_backend.repositories.student_skill_repository import StudentSkillRepository
from app_backend.repositories.user_repository import UserRepository
from app_backend.schemas.profile import CVDataUpdate, DepartmentInfo, SkillInfo, StudentProfileResponse


class IProfileService(Protocol):
    def get_student_profile(self, user_id: uuid.UUID) -> Optional[StudentProfileResponse]: ...
    def update_cv_data(self, user_id: uuid.UUID, data: CVDataUpdate) -> None: ...


class ProfileService:
    def __init__(
        self,
        student_repo: StudentRepository,
        user_repo: UserRepository,
        student_skill_repo: StudentSkillRepository,
    ):
        self.student_repo = student_repo
        self.user_repo = user_repo
        self.student_skill_repo = student_skill_repo

    def get_student_profile(self, user_id: uuid.UUID) -> Optional[StudentProfileResponse]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        # Custom query with eager loading for efficiency (Abstraction of complex join)
        profile = (
            self.student_repo.session.query(ProfilesStudent)
            .options(
                joinedload(ProfilesStudent.department),
                selectinload(ProfilesStudent.student_skills).joinedload(StudentSkills.skill),
            )
            .filter(ProfilesStudent.user_id == user_id)
            .first()
        )

        if not profile:
            return None

        dept_info = None
        if profile.department:
            dept_info = DepartmentInfo(
                id=profile.department.id,
                code=profile.department.code,
                name=profile.department.name,
                faculty=profile.department.faculty,
            )

        skills = [
            SkillInfo(
                skill_id=ss.skill_id,
                skill_name=ss.skill.name,
                skill_category=ss.skill.category,
                level=ss.level or 1,
            )
            for ss in profile.student_skills
            if ss.skill
        ]

        return StudentProfileResponse(
            user_id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active if user.is_active is not None else True,
            nim=profile.nim,
            full_name=profile.full_name,
            semester=profile.semester,
            department=dept_info,
            gpa=profile.gpa,
            is_mbkm_eligible=(profile.is_mbkm_eligible if profile.is_mbkm_eligible is not None else True),
            phone_number=profile.phone_number,
            linkedin_url=profile.linkedin_url,
            cv_url=profile.cv_url,
            avatar_url=profile.avatar_url,
            skills=skills,
            updated_at=profile.updated_at,
        )

    def update_cv_data(self, user_id: uuid.UUID, data: CVDataUpdate) -> None:
        profile = self.student_repo.get_by_id(user_id)
        if not profile:
            raise ValueError("Profil mahasiswa tidak ditemukan")

        try:
            if data.phone_number is not None:
                profile.phone_number = data.phone_number
            if data.linkedin_url is not None:
                profile.linkedin_url = str(data.linkedin_url)
            has_run_sync = False
            if data.cv_url is not None:
                from app_backend.conf.settings import settings
                if settings.is_development:
                    try:
                        from app_backend.shared.tasks.ai_tasks import parse_cv_skills_sync
                        secured_cv_url = parse_cv_skills_sync(str(user_id), str(data.cv_url), self.student_repo.session)
                        profile.cv_url = secured_cv_url
                        has_run_sync = True
                    except Exception as sync_err:
                        print(f"Failed to parse CV synchronously in dev: {sync_err}. Falling back to saving raw URL.")
                        profile.cv_url = str(data.cv_url)
                else:
                    profile.cv_url = str(data.cv_url)

            if data.skills is not None:
                self.student_skill_repo.delete_all_for_student(user_id)
                for s in data.skills:
                    self.student_skill_repo.create(StudentSkills(student_id=user_id, skill_id=s.skill_id, level=s.level))

            profile.updated_at = datetime.now(timezone.utc)
            self.student_repo.save_changes()

            if data.cv_url is not None and not has_run_sync:
                try:
                    from app_backend.shared.tasks.ai_tasks import parse_cv_skills
                    parse_cv_skills.delay(str(user_id), str(data.cv_url))
                except Exception as e:
                    print(f"Failed to queue CV parsing: {e}")
        except Exception as exc:
            self.student_repo.rollback()
            raise exc
