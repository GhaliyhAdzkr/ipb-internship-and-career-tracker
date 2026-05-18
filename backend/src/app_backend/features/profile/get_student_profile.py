from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session, joinedload, selectinload

from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.student_skills import StudentSkills
from app_backend.models.users import Users
from app_backend.schemas.profile import DepartmentInfo, SkillInfo, StudentProfileResponse


@dataclass
class GetStudentProfileCommand:
    user_id: uuid.UUID


@dataclass
class GetStudentProfileResult:
    profile: Optional[StudentProfileResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def get_student_profile_command_handler(
    command: GetStudentProfileCommand,
    session: Session,
) -> GetStudentProfileResult:
    """
    Business Rules:
    1. User harus ada di auth.users.
    2. Profil mahasiswa harus ada di profiles_student.
    3. Eager-load department (optional) dan student_skills + skill.
    """
    user = session.query(Users).filter(Users.id == command.user_id).first()
    if not user:
        return GetStudentProfileResult(error_message="User tidak ditemukan")

    profile = (
        session.query(ProfilesStudent)
        .options(
            joinedload(ProfilesStudent.department),
            selectinload(ProfilesStudent.student_skills).joinedload(StudentSkills.skill),
        )
        .filter(ProfilesStudent.user_id == command.user_id)
        .first()
    )
    if not profile:
        return GetStudentProfileResult(error_message="Profil mahasiswa tidak ditemukan")

    department_info = None
    if profile.department:
        department_info = DepartmentInfo(
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

    return GetStudentProfileResult(
        profile=StudentProfileResponse(
            user_id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active if user.is_active is not None else True,
            nim=profile.nim,
            full_name=profile.full_name,
            semester=profile.semester,
            department=department_info,
            gpa=profile.gpa,
            is_mbkm_eligible=(profile.is_mbkm_eligible if profile.is_mbkm_eligible is not None else True),
            phone_number=profile.phone_number,
            linkedin_url=profile.linkedin_url,
            cv_url=profile.cv_url,
            skills=skills,
            updated_at=profile.updated_at,
        )
    )
