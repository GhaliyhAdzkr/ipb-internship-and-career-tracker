"""
Update CV Data Feature - Command Handler
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.student_skills import StudentSkills
from app_backend.models.master_skills import MasterSkills
from app_backend.schemas.profile import CVDataUpdate
from app_backend.domain.student import Student


@dataclass
class UpdateCVDataCommand:
    """Command untuk update CV data mahasiswa"""
    user_id: UUID
    payload: CVDataUpdate


@dataclass
class UpdateCVDataResult:
    """Result dari update CV data"""
    success: bool = False
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def update_cv_data_command_handler(
    command: UpdateCVDataCommand,
    session: Session
) -> UpdateCVDataResult:
    """
    Handle update CV data mahasiswa
    
    Business Rules:
    1. Profile student harus ada
    2. Validasi data melalui domain model
    3. Update phone_number, linkedin_url, cv_url jika diberikan
    4. Update skills: delete existing, insert new
    5. Validasi skill_id harus ada di master_skills
    """
    
    try:
        # Query profile student
        profile = session.query(ProfilesStudent).filter(
            ProfilesStudent.user_id == command.user_id
        ).first()
        
        if not profile:
            return UpdateCVDataResult(
                error_message="Profile mahasiswa tidak ditemukan"
            )
        
        # Convert ke domain model untuk validasi
        domain_student = profile.to_domain()
        
        # Update profile data using domain logic (untuk validasi)
        phone_str = str(command.payload.phone_number) if command.payload.phone_number else None
        linkedin_str = str(command.payload.linkedin_url) if command.payload.linkedin_url else None
        cv_str = str(command.payload.cv_url) if command.payload.cv_url else None
        
        domain_student.update_profile(
            phone_number=phone_str,
            linkedin_url=linkedin_str,
            cv_url=cv_str
        )
        
        # Update ORM model
        if command.payload.phone_number is not None:
            profile.phone_number = phone_str
        
        if command.payload.linkedin_url is not None:
            profile.linkedin_url = linkedin_str
        
        if command.payload.cv_url is not None:
            profile.cv_url = cv_str
        
        profile.updated_at = datetime.utcnow()
        
        # Update skills jika diberikan
        if command.payload.skills is not None:
            # Validate all skill_ids exist first
            skill_ids = [skill.skill_id for skill in command.payload.skills]
            existing_skills = session.query(MasterSkills).filter(
                MasterSkills.id.in_(skill_ids)
            ).all()
            
            existing_skill_ids = {skill.id for skill in existing_skills}
            invalid_skill_ids = set(skill_ids) - existing_skill_ids
            
            if invalid_skill_ids:
                return UpdateCVDataResult(
                    error_message=f"Skill ID tidak valid: {invalid_skill_ids}"
                )
            
            # Delete existing skills
            session.query(StudentSkills).filter(
                StudentSkills.student_id == command.user_id
            ).delete()
            
            # Insert new skills
            for skill_data in command.payload.skills:
                new_skill = StudentSkills(
                    student_id=command.user_id,
                    skill_id=skill_data.skill_id,
                    level=skill_data.level
                )
                session.add(new_skill)
        
        session.commit()
        
        return UpdateCVDataResult(
            success=True,
            message="CV data berhasil diupdate"
        )
        
    except ValueError as e:
        session.rollback()
        return UpdateCVDataResult(
            error_message=f"Validasi gagal: {str(e)}"
        )
    except Exception as e:
        session.rollback()
        return UpdateCVDataResult(
            error_message=f"Error update CV data: {str(e)}"
        )
