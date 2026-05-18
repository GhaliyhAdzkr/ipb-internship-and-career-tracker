from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Optional

from fastapi import UploadFile

from app_backend.shared.s3_storage import get_s3_client, upload_fileobj
from app_backend.conf.settings import settings

UPLOAD_DIR = "companies-logo"


@dataclass
class UploadCompanyLogoCommand:
    file: UploadFile


@dataclass
class UploadCompanyLogoResult:
    logo_url: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def upload_company_logo_command_handler(
    command: UploadCompanyLogoCommand,
) -> UploadCompanyLogoResult:
    """
    Business Rules:
    1. File image (png, jpg, webp, jpeg).
    2. File size max 10MB.
    """
    file = command.file

    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
    if file.content_type not in allowed_types:
        return UploadCompanyLogoResult(error_message="Format file tidak didukung. Gunakan JPG, PNG, atau WEBP.")

    file_ext = ""
    if file.filename:
        _, file_ext = os.path.splitext(file.filename)
    if not file_ext:
        file_ext = ".jpg"  # default

    # Generate unique filename
    unique_filename = f"logo_{uuid.uuid4().hex[:8]}{file_ext.lower()}"
    s3_key = f"{UPLOAD_DIR}/{unique_filename}"

    try:
        # Check size before upload
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if file_size > MAX_SIZE:
            return UploadCompanyLogoResult(error_message="Ukuran file melebihi batas maksimal 10MB")

        if settings.storage_type == "s3":
            s3_client = get_s3_client()
            success = upload_fileobj(s3_client, file.file, settings.s3_bucket, s3_key, content_type=file.content_type)
            if not success:
                return UploadCompanyLogoResult(error_message="Gagal mengunggah file ke storage S3")

            # Construct public URL (for Supabase Storage S3 gateway)
            if "storage.supabase.co/storage/v1/s3" in settings.s3_endpoint:
                public_endpoint = settings.s3_endpoint.replace("/storage/v1/s3", "/storage/v1/object/public")
                logo_url = f"{public_endpoint}/{settings.s3_bucket}/{s3_key}"
            else:
                logo_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"
        else:
            # Fallback to local
            os.makedirs(f"uploads/{UPLOAD_DIR}", exist_ok=True)
            file_path = os.path.join(f"uploads/{UPLOAD_DIR}", unique_filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            logo_url = f"/uploads/{UPLOAD_DIR}/{unique_filename}"

        return UploadCompanyLogoResult(logo_url=logo_url, message="Logo berhasil diupload")

    except Exception as exc:
        return UploadCompanyLogoResult(error_message=f"Upload gagal: {exc}")
