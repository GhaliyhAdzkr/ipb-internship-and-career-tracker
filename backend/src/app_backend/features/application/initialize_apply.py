import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.applications import Applications
from app_backend.models.profiles_student import ProfilesStudent
from app_backend.schemas.application import ApplicationCreate, ApplicationResponse


@dataclass
class InitializeApplyCommand:
    student_id: uuid.UUID
    payload: ApplicationCreate


@dataclass
class InitializeApplyResult:
    application: Optional[ApplicationResponse] = None
    error_message: Optional[str] = None

    def get_error_message(self) -> Optional[str]:
        return self.error_message


def initialize_apply_command_handler(command: InitializeApplyCommand, session: Session) -> InitializeApplyResult:

    # 1. Fetch student profile to get cv_url
    student = session.get(ProfilesStudent, command.student_id)
    if student is None:
        return InitializeApplyResult(error_message="Student profile not found.")

    if not student.cv_url:
        return InitializeApplyResult(error_message="You must upload a CV before applying to a vacancy.")

    # 2. Check for duplicate application

    existing = session.query(Applications).filter_by(vacancy_id=command.payload.vacancy_id, student_id=command.student_id).first()

    if existing:
        return InitializeApplyResult(error_message="You have already applied to this vacancy.")

    # 3. Insert into public.applications
    application = Applications(
        vacancy_id=command.payload.vacancy_id,
        student_id=command.student_id,
        cv_snapshot_url=student.cv_url,  # snapshot of the CV at the time of application
    )

    session.add(application)
    session.commit()
    session.refresh(application)

    return InitializeApplyResult(application=ApplicationResponse.model_validate(application))
