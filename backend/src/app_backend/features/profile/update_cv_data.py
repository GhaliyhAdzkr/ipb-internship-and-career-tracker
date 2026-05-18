from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.profiles_student import ProfilesStudent
from app_backend.models.student_skills import StudentSkills
from app_backend.schemas.profile import CVDataUpdate


@dataclass
class UpdateCVDataCommand:
    user_id: uuid.UUID
    payload: CVDataUpdate


@dataclass
class UpdateCVDataResult:
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def update_cv_data_command_handler(
    command: UpdateCVDataCommand,
    session: Session,
) -> UpdateCVDataResult:
    """
    Business Rules:
    1. Profil mahasiswa harus ada.
    2. PATCH semantics: hanya field yang dikirim yang diupdate.
    3. Jika `skills` disediakan: full replace (hapus semua, insert baru).
       Skill ID harus valid – FK constraint di DB akan menolak jika tidak ada.
    """
    profile = session.query(ProfilesStudent).filter(ProfilesStudent.user_id == command.user_id).first()
    if not profile:
        return UpdateCVDataResult(error_message="Profil mahasiswa tidak ditemukan")

    try:
        payload = command.payload

        if payload.phone_number is not None:
            profile.phone_number = payload.phone_number
        if payload.linkedin_url is not None:
            profile.linkedin_url = str(payload.linkedin_url)
        from app_backend.conf.settings import settings

        has_run_sync = False
        if payload.cv_url is not None:
            if settings.is_development:
                try:
                    from app_backend.shared.tasks.ai_tasks import parse_cv_skills_sync

                    secured_cv_url = parse_cv_skills_sync(str(command.user_id), str(payload.cv_url), session)
                    profile.cv_url = secured_cv_url
                    has_run_sync = True
                except Exception as sync_err:
                    print(f"Failed to parse CV synchronously in dev: {sync_err}. Falling back to saving raw URL.")
                    profile.cv_url = str(payload.cv_url)
            else:
                # In Production/Staging: Save raw link immediately, background queue will host and parse it
                profile.cv_url = str(payload.cv_url)

        if payload.skills is not None:
            # Full replace hapus semua skill lama, insert baru
            session.query(StudentSkills).filter(StudentSkills.student_id == command.user_id).delete(synchronize_session="fetch")

            for skill_data in payload.skills:
                session.add(
                    StudentSkills(
                        student_id=command.user_id,
                        skill_id=skill_data.skill_id,
                        level=skill_data.level,
                    )
                )

        profile.updated_at = datetime.now(timezone.utc)
        session.commit()

        # Trigger CV parsing task in background only as fallback if synchronous execution failed
        if payload.cv_url and not has_run_sync:
            try:
                from app_backend.shared.tasks.ai_tasks import parse_cv_skills

                parse_cv_skills.delay(str(command.user_id), str(payload.cv_url))
            except Exception as e:
                # Do not block the profile save if Celery/Redis is not running
                print(f"Failed to queue CV parsing: {e}")

        return UpdateCVDataResult(message="Data CV berhasil diperbarui")

    except Exception as exc:
        session.rollback()
        return UpdateCVDataResult(error_message=f"Update gagal: {exc}")
