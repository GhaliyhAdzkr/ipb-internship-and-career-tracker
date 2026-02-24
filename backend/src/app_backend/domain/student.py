"""
Domain Model untuk Student
Model domain yang berisi business logic untuk mahasiswa
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Student:
    """Domain model untuk Student Profile"""

    user_id: uuid.UUID
    nim: str
    full_name: str
    semester: int
    department_id: Optional[uuid.UUID] = None
    gpa: Optional[Decimal] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    cv_url: Optional[str] = None
    is_mbkm_eligible: bool = False
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validasi domain rules"""
        # Validasi NIM
        if not self.nim or len(self.nim) < 6:
            raise ValueError("NIM tidak valid (minimal 6 karakter)")

        # Validasi nama
        if not self.full_name or len(self.full_name) < 3:
            raise ValueError("Nama lengkap harus diisi (minimal 3 karakter)")

        # Validasi semester
        if self.semester < 1 or self.semester > 14:
            raise ValueError("Semester harus antara 1-14")

        # Validasi GPA jika ada
        if self.gpa is not None:
            if self.gpa < 0 or self.gpa > 4:
                raise ValueError("GPA harus antara 0.00-4.00")

        # Validasi phone number format jika ada
        if self.phone_number:
            # Hapus karakter non-digit
            digits_only = "".join(filter(str.isdigit, self.phone_number))
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError("Nomor telepon tidak valid (10-15 digit)")

        # Set timestamp jika belum ada
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def update_gpa(self, new_gpa: Decimal):
        """Update GPA mahasiswa"""
        if new_gpa < 0 or new_gpa > 4:
            raise ValueError("GPA harus antara 0.00-4.00")
        self.gpa = new_gpa
        self.updated_at = datetime.utcnow()

    def advance_semester(self):
        """Naikkan semester mahasiswa"""
        if self.semester >= 14:
            raise ValueError("Semester sudah maksimal")
        self.semester += 1
        self.updated_at = datetime.utcnow()

    def is_eligible_for_internship(self) -> bool:
        """Cek apakah mahasiswa eligible untuk magang

        Kriteria:
        - Semester minimal 5
        - GPA minimal 2.5 (jika GPA sudah diisi)
        """
        if self.semester < 5:
            return False

        if self.gpa is not None and self.gpa < Decimal("2.5"):
            return False

        return True

    def is_eligible_for_mbkm(self) -> bool:
        """Cek apakah mahasiswa eligible untuk MBKM

        Kriteria:
        - Semester minimal 5
        - Semester maksimal 7
        - GPA minimal 3.0
        - Flag is_mbkm_eligible True
        """
        if not self.is_mbkm_eligible:
            return False

        if self.semester < 5 or self.semester > 7:
            return False

        if self.gpa is None or self.gpa < Decimal("3.0"):
            return False

        return True

    def update_profile(
        self,
        phone_number: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        cv_url: Optional[str] = None,
    ):
        """Update profil mahasiswa"""
        if phone_number is not None:
            # Validasi phone number
            digits_only = "".join(filter(str.isdigit, phone_number))
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError("Nomor telepon tidak valid (10-15 digit)")
            self.phone_number = phone_number

        if linkedin_url is not None:
            self.linkedin_url = linkedin_url

        if cv_url is not None:
            self.cv_url = cv_url

        self.updated_at = datetime.utcnow()
