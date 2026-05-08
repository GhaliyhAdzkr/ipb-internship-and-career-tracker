"""
Domain Model untuk Application
Model domain yang berisi business logic untuk lamaran kerja/magang
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class ApplicationStatus(str, Enum):
    """Enum untuk status aplikasi"""

    APPLIED = "APPLIED"
    SCREENING = "SCREENING"
    INTERVIEW = "INTERVIEW"
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


@dataclass
class Application:
    """Domain model untuk Application (Lamaran)"""

    id: uuid.UUID
    vacancy_id: uuid.UUID
    student_id: uuid.UUID
    status: str = ApplicationStatus.APPLIED.value
    match_percentage: Optional[Decimal] = None
    cv_snapshot_url: Optional[str] = None
    applied_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validasi domain rules"""
        # Validasi status
        valid_statuses = [s.value for s in ApplicationStatus]
        if self.status not in valid_statuses:
            raise ValueError(f"Status tidak valid. Pilih salah satu: {', '.join(valid_statuses)}")

        # Validasi match percentage jika ada
        if self.match_percentage is not None:
            if self.match_percentage < 0 or self.match_percentage > 100:
                raise ValueError("Match percentage harus antara 0-100")

        # Set timestamps jika belum ada
        if self.applied_at is None:
            self.applied_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def update_status(self, new_status: str):
        """Update status aplikasi dengan validasi business rules"""
        valid_statuses = [s.value for s in ApplicationStatus]
        if new_status not in valid_statuses:
            raise ValueError(f"Status tidak valid: {new_status}")

        # Validasi state transition
        if self.status == ApplicationStatus.WITHDRAWN.value:
            raise ValueError("Aplikasi yang sudah di-withdraw tidak bisa diupdate")

        if self.status == ApplicationStatus.ACCEPTED.value and new_status != ApplicationStatus.WITHDRAWN.value:
            raise ValueError("Aplikasi yang sudah diterima hanya bisa di-withdraw")

        if self.status == ApplicationStatus.REJECTED.value:
            raise ValueError("Aplikasi yang sudah ditolak tidak bisa diupdate")

        self.status = new_status
        self.updated_at = datetime.utcnow()

    def withdraw(self):
        """Mahasiswa menarik aplikasi"""
        if self.status in [
            ApplicationStatus.REJECTED.value,
            ApplicationStatus.WITHDRAWN.value,
        ]:
            raise ValueError("Aplikasi tidak bisa di-withdraw")

        self.status = ApplicationStatus.WITHDRAWN.value
        self.updated_at = datetime.utcnow()

    def move_to_screening(self):
        """Pindahkan ke tahap screening"""
        if self.status != ApplicationStatus.APPLIED.value:
            raise ValueError("Hanya aplikasi dengan status APPLIED yang bisa dipindah ke SCREENING")
        self.update_status(ApplicationStatus.SCREENING.value)

    def move_to_interview(self):
        """Pindahkan ke tahap interview"""
        if self.status not in [
            ApplicationStatus.APPLIED.value,
            ApplicationStatus.SCREENING.value,
        ]:
            raise ValueError("Status tidak valid untuk dipindah ke INTERVIEW")
        self.update_status(ApplicationStatus.INTERVIEW.value)

    def offer(self):
        """Berikan penawaran kepada kandidat"""
        if self.status not in [
            ApplicationStatus.SCREENING.value,
            ApplicationStatus.INTERVIEW.value,
        ]:
            raise ValueError("Status tidak valid untuk memberikan penawaran")
        self.update_status(ApplicationStatus.OFFERED.value)

    def accept(self):
        """Kandidat menerima penawaran"""
        if self.status != ApplicationStatus.OFFERED.value:
            raise ValueError("Hanya aplikasi dengan status OFFERED yang bisa diterima")
        self.update_status(ApplicationStatus.ACCEPTED.value)

    def reject(self):
        """Perusahaan menolak aplikasi"""
        if self.status in [
            ApplicationStatus.ACCEPTED.value,
            ApplicationStatus.REJECTED.value,
            ApplicationStatus.WITHDRAWN.value,
        ]:
            raise ValueError("Aplikasi tidak bisa ditolak")
        self.update_status(ApplicationStatus.REJECTED.value)

    def is_active(self) -> bool:
        """Cek apakah aplikasi masih aktif (belum final)"""
        return self.status not in [
            ApplicationStatus.ACCEPTED.value,
            ApplicationStatus.REJECTED.value,
            ApplicationStatus.WITHDRAWN.value,
        ]

    def is_successful(self) -> bool:
        """Cek apakah aplikasi berhasil (diterima)"""
        return self.status == ApplicationStatus.ACCEPTED.value

    def set_match_percentage(self, percentage: Decimal):
        """Set persentase kesesuaian kandidat dengan lowongan"""
        if percentage < 0 or percentage > 100:
            raise ValueError("Match percentage harus antara 0-100")
        self.match_percentage = percentage
        self.updated_at = datetime.utcnow()
