"""
Upload CV Feature – Command Handler.
Upload file CV PDF dan simpan URL ke database.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app_backend.models.profiles_student import ProfilesStudent
from app_backend.shared.s3_storage import get_s3_client, upload_fileobj
from app_backend.conf.settings import settings

UPLOAD_DIR = "cv"


@dataclass
class UploadCVCommand:
    user_id: uuid.UUID
    file: UploadFile


@dataclass
class UploadCVResult:
    cv_url: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def upload_cv_command_handler(
    command: UploadCVCommand,
    session: Session,
) -> UploadCVResult:
    """
    Business Rules:
    1. Profil mahasiswa harus ada.
    2. File harus PDF.
    3. File size limit (ditangani oleh fastapi tapi baiknya double check, max 10MB).
    """
    profile = session.query(ProfilesStudent).filter(ProfilesStudent.user_id == command.user_id).first()
    if not profile:
        return UploadCVResult(error_message="Profil mahasiswa tidak ditemukan")

    file = command.file
    if file.content_type != "application/pdf":
        return UploadCVResult(error_message="File harus berformat PDF")

    if not (command.file.filename and command.file.filename.lower().endswith(".pdf")):
        return UploadCVResult(error_message="Ekstensi file tidak diizinkan, harus .pdf")

    # Generate unique filename
    file_ext = ".pdf"
    unique_filename = f"{command.user_id}_{uuid.uuid4().hex[:8]}{file_ext}"
    s3_key = f"{UPLOAD_DIR}/{unique_filename}"

    try:
        # Check size before upload (FastAPI UploadFile might already have it in memory or spooled)
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if file_size > MAX_SIZE:
            return UploadCVResult(error_message="Ukuran file melebihi batas maksimal 10MB")

        if settings.storage_type == "s3":
            s3_client = get_s3_client()
            success = upload_fileobj(s3_client, file.file, settings.s3_bucket, s3_key, content_type="application/pdf")
            if not success:
                return UploadCVResult(error_message="Gagal mengunggah file ke storage S3")

            # Construct public URL (for Supabase Storage S3 gateway)
            if "storage.supabase.co/storage/v1/s3" in settings.s3_endpoint:
                public_endpoint = settings.s3_endpoint.replace("/storage/v1/s3", "/storage/v1/object/public")
                cv_url = f"{public_endpoint}/{settings.s3_bucket}/{s3_key}"
            else:
                cv_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"
        else:
            # Fallback to local
            os.makedirs(f"uploads/{UPLOAD_DIR}", exist_ok=True)
            file_path = os.path.join(f"uploads/{UPLOAD_DIR}", unique_filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            cv_url = f"/uploads/{UPLOAD_DIR}/{unique_filename}"

        profile.cv_url = cv_url
        profile.updated_at = datetime.now(timezone.utc)

        session.commit()
        return UploadCVResult(cv_url=cv_url, message="CV berhasil diupload")

    except Exception as exc:
        session.rollback()
        return UploadCVResult(error_message=f"Upload gagal: {exc}")
