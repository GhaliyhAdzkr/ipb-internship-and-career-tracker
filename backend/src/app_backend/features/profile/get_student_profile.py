"""
Get Student Profile Feature - Command Handler
"""
from dataclasses import dataclass
from typing import Optional, List, Dict
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app_backend.models.users import Users
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.student_skills import StudentSkills
from app_backend.models.master_skills import MasterSkills
from app_backend.schemas.profile import StudentProfileResponse, DepartmentInfo, SkillInfo


@dataclass
class GetStudentProfileCommand:
    """Command untuk mengambil profil mahasiswa"""
    user_id: UUID


@dataclass
class GetStudentProfileResult:
    """Result dari get student profile"""
    profile: Optional[StudentProfileResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def get_student_profile_command_handler(
    command: GetStudentProfileCommand,
    session: Session
) -> GetStudentProfileResult:
    """
    Handle get student profile
    
    Business Rules:
    1. User harus ada dan aktif
    2. User harus memiliki role STUDENT
    3. Profile student harus sudah dibuat
    4. Load semua relasi: department, skills
    """
    
    try:
        # Query user dengan eager loading
        user = session.query(Users).filter(
            Users.id == command.user_id
        ).first()
        
        if not user:
            return GetStudentProfileResult(
                error_message="User tidak ditemukan"
            )
        
        if not user.is_active:
            return GetStudentProfileResult(
                error_message="User tidak aktif"
            )
        
        if user.role != "STUDENT":
            return GetStudentProfileResult(
                error_message="User bukan mahasiswa"
            )
        
        # Query profile student dengan eager loading
        profile = session.query(ProfilesStudent).options(
            joinedload(ProfilesStudent.department),
            joinedload(ProfilesStudent.student_skills).joinedload(StudentSkills.skill)
        ).filter(
            ProfilesStudent.user_id == command.user_id
        ).first()
        
        if not profile:
            return GetStudentProfileResult(
                error_message="Profile mahasiswa belum dibuat"
            )
        
        # Build department info
        department_info = None
        if profile.department:
            department_info = DepartmentInfo(
                id=profile.department.id,
                code=profile.department.code,
                name=profile.department.name,
                faculty=profile.department.faculty
            )
        
        # Build skills info
        skills_info = []
        for student_skill in profile.student_skills:
            skills_info.append(SkillInfo(
                skill_id=student_skill.skill_id,
                skill_name=student_skill.skill.name,
                skill_category=student_skill.skill.category,
                level=student_skill.level
            ))
        
        # Build response
        response = StudentProfileResponse(
            user_id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            nim=profile.nim,
            full_name=profile.full_name,
            semester=profile.semester,
            department=department_info,
            gpa=profile.gpa,
            is_mbkm_eligible=profile.is_mbkm_eligible,
            phone_number=profile.phone_number,
            linkedin_url=profile.linkedin_url,
            cv_url=profile.cv_url,
            skills=skills_info,
            updated_at=profile.updated_at
        )
        
        return GetStudentProfileResult(profile=response)
        
    except Exception as e:
        session.rollback()
        return GetStudentProfileResult(
            error_message=f"Error mengambil profile: {str(e)}"
        )
