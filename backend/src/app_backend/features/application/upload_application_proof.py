import os
import uuid
from dataclasses import dataclass
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app_backend.models.applications import Applications
from app_backend.shared.s3_storage import get_s3_client, upload_fileobj
from app_backend.conf.settings import settings

UPLOAD_DIR = "proofs"


@dataclass
class UploadApplicationProofCommand:
    application_id: uuid.UUID
    student_id: uuid.UUID
    file: UploadFile


@dataclass
class UploadApplicationProofResult:
    proof_url: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def upload_application_proof_command_handler(
    command: UploadApplicationProofCommand,
    session: Session,
) -> UploadApplicationProofResult:
    """
    Business Rules:
    1. Hanya menerima image/jpeg, image/png, application/pdf.
    2. Ukuran maksimum 10MB.
    3. Endpoint ini hanya bisa dipanggil jika application.status = ACCEPTED
    """
    application = session.query(Applications).filter_by(id=command.application_id, student_id=command.student_id).first()
    if not application:
        return UploadApplicationProofResult(error_message="Lamaran tidak ditemukan")

    if application.status != "ACCEPTED":
        return UploadApplicationProofResult(error_message="Status lamaran harus ACCEPTED untuk mengunggah bukti")

    file = command.file
    valid_content_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in valid_content_types:
        return UploadApplicationProofResult(error_message="File harus berupa image/jpeg, image/png, atau application/pdf")

    # Extension check
    filename = file.filename.lower()
    if not (filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".pdf")):
        return UploadApplicationProofResult(error_message="Ekstensi file tidak valid")

    ext = os.path.splitext(filename)[1]
    unique_filename = f"proof_{command.application_id}_{uuid.uuid4().hex[:8]}{ext}"
    s3_key = f"{UPLOAD_DIR}/{unique_filename}"

    try:
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if file_size > MAX_SIZE:
            return UploadApplicationProofResult(error_message="Ukuran file melebihi batas maksimal 10MB")

        if settings.storage_type == "s3":
            s3_client = get_s3_client()
            success = upload_fileobj(s3_client, file.file, settings.s3_bucket, s3_key, content_type=file.content_type)
            if not success:
                return UploadApplicationProofResult(error_message="Gagal mengunggah bukti ke storage S3")

            proof_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"
        else:
            os.makedirs(f"uploads/{UPLOAD_DIR}", exist_ok=True)
            file_path = os.path.join(f"uploads/{UPLOAD_DIR}", unique_filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            proof_url = f"/uploads/{UPLOAD_DIR}/{unique_filename}"

        # Trigger an update to insert into application_logs
        from sqlalchemy import text

        session.execute(
            text("""
            INSERT INTO application_logs (id, application_id, previous_status, new_status, changed_by, proof_url, reason)
            VALUES (:id, :app_id, :status, :status, :by, :proof, 'Upload Bukti')
            """),
            {
                "id": uuid.uuid4(),
                "app_id": application.id,
                "status": application.status,
                "by": command.student_id,
                "proof": proof_url,
            },
        )

        session.commit()
        return UploadApplicationProofResult(proof_url=proof_url, message="Bukti berhasil diunggah")

    except Exception as exc:
        session.rollback()
        return UploadApplicationProofResult(error_message=f"Upload gagal: {exc}")
