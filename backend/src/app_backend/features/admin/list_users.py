from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app_backend.models.users import Users
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.master_departments import MasterDepartments
from app_backend.schemas.user import UserResponse


@dataclass
class ListUsersCommand:
    role: Optional[str] = None


@dataclass
class ListUsersResult:
    items: List[UserResponse]
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_users_command_handler(command: ListUsersCommand, session: Session) -> ListUsersResult:
    try:
        query = session.query(Users).options(
            joinedload(Users.profile_student).joinedload(ProfilesStudent.department)
        )
        
        if command.role:
            query = query.filter(Users.role == command.role)
            
        users = query.all()
        
        items = []
        for u in users:
            # Map manually to UserResponse
            student_profile = u.profile_student
            items.append(UserResponse(
                id=u.id,
                email=u.email,
                role=u.role,
                is_active=u.is_active,
                full_name=student_profile.full_name if student_profile else u.profile_admin.full_name if u.profile_admin else None,
                nim=student_profile.nim if student_profile else None,
                semester=student_profile.semester if student_profile else None,
                phone_number=student_profile.phone_number if student_profile else None,
                linkedin_url=student_profile.linkedin_url if student_profile else None,
                gpa=student_profile.gpa if student_profile else None,
                department_id=student_profile.department_id if student_profile else None,
                department_name=student_profile.department.name if student_profile and student_profile.department else None,
                last_login_at=u.last_login_at,
                created_at=u.created_at,
                updated_at=u.updated_at
            ))
            
        return ListUsersResult(items=items)
    except Exception as e:
        return ListUsersResult(items=[], error_message=str(e))
