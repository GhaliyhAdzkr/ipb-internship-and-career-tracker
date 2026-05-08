"""
Domain Model untuk Vacancy
Model domain yang berisi business logic untuk lowongan kerja/magang
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class VacancyType(str, Enum):
    """Enum untuk tipe lowongan"""

    INTERNSHIP_GENERAL = "INTERNSHIP_GENERAL"
    MBKM_INTERNSHIP = "MBKM_INTERNSHIP"
    MBKM_STUDY_INDEPENDENT = "MBKM_STUDY_INDEPENDENT"
    FULL_TIME = "FULL_TIME"


@dataclass
class Vacancy:
    """Domain model untuk Vacancy (Lowongan)"""

    id: uuid.UUID
    company_id: uuid.UUID
    title: str
    description: str
    type: str
    open_date: datetime
    close_date: datetime
    location: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    is_auto_close: bool = True
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validasi domain rules"""
        # Validasi title
        if not self.title or len(self.title) < 5:
            raise ValueError("Judul lowongan minimal 5 karakter")

        # Validasi description
        if not self.description or len(self.description) < 20:
            raise ValueError("Deskripsi lowongan minimal 20 karakter")

        # Validasi type
        valid_types = [vt.value for vt in VacancyType]
        if self.type not in valid_types:
            raise ValueError(f"Tipe lowongan tidak valid. Pilih salah satu: {', '.join(valid_types)}")

        # Validasi tanggal
        if self.open_date >= self.close_date:
            raise ValueError("Tanggal tutup harus setelah tanggal buka")

        # Validasi salary
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_min > self.salary_max:
                raise ValueError("Gaji minimum tidak boleh lebih besar dari gaji maksimum")
            if self.salary_min < 0:
                raise ValueError("Gaji minimum tidak boleh negatif")

        # Set timestamps jika belum ada
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def activate(self):
        """Aktifkan lowongan"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        """Nonaktifkan lowongan"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def is_open(self) -> bool:
        """Cek apakah lowongan masih terbuka"""
        now = datetime.utcnow()

        # Cek status aktif
        if not self.is_active:
            return False

        # Cek tanggal
        if now < self.open_date or now > self.close_date:
            return False

        return True

    def is_expired(self) -> bool:
        """Cek apakah lowongan sudah kadaluarsa"""
        return datetime.utcnow() > self.close_date

    def extend_deadline(self, new_close_date: datetime):
        """Perpanjang deadline lowongan"""
        if new_close_date <= self.close_date:
            raise ValueError("Tanggal penutupan baru harus lebih lama dari sekarang")

        if new_close_date <= datetime.utcnow():
            raise ValueError("Tanggal penutupan tidak boleh di masa lalu")

        self.close_date = new_close_date
        self.updated_at = datetime.utcnow()

    def update_details(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        salary_min: Optional[Decimal] = None,
        salary_max: Optional[Decimal] = None,
    ):
        """Update detail lowongan"""
        if title is not None:
            if len(title) < 5:
                raise ValueError("Judul lowongan minimal 5 karakter")
            self.title = title

        if description is not None:
            if len(description) < 20:
                raise ValueError("Deskripsi lowongan minimal 20 karakter")
            self.description = description

        if location is not None:
            self.location = location

        if salary_min is not None:
            if salary_min < 0:
                raise ValueError("Gaji minimum tidak boleh negatif")
            self.salary_min = salary_min

        if salary_max is not None:
            if salary_max < 0:
                raise ValueError("Gaji maksimum tidak boleh negatif")
            self.salary_max = salary_max

        # Validasi salary range jika keduanya ada
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_min > self.salary_max:
                raise ValueError("Gaji minimum tidak boleh lebih besar dari gaji maksimum")

        self.updated_at = datetime.utcnow()

    def is_mbkm_program(self) -> bool:
        """Cek apakah ini program MBKM"""
        return self.type in [
            VacancyType.MBKM_INTERNSHIP.value,
            VacancyType.MBKM_STUDY_INDEPENDENT.value,
        ]
