"""
Domain Model untuk Company
Model domain yang berisi business logic untuk perusahaan
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Company:
    """Domain model untuk Company Profile"""

    user_id: uuid.UUID
    company_name: str
    industry: Optional[str] = None
    website_url: Optional[str] = None
    address: Optional[str] = None
    is_verified: bool = False
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validasi domain rules"""
        # Validasi nama perusahaan
        if not self.company_name or len(self.company_name) < 3:
            raise ValueError("Nama perusahaan harus diisi (minimal 3 karakter)")

        # Validasi website URL jika ada
        if self.website_url:
            if not (
                self.website_url.startswith("http://")
                or self.website_url.startswith("https://")
            ):
                raise ValueError("URL website harus valid (http:// atau https://)")

        # Set timestamp jika belum ada
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def verify(self):
        """Verifikasi perusahaan"""
        self.is_verified = True
        self.updated_at = datetime.utcnow()

    def unverify(self):
        """Batalkan verifikasi perusahaan"""
        self.is_verified = False
        self.updated_at = datetime.utcnow()

    def update_profile(
        self,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        website_url: Optional[str] = None,
        address: Optional[str] = None,
    ):
        """Update profil perusahaan"""
        if company_name is not None:
            if len(company_name) < 3:
                raise ValueError("Nama perusahaan minimal 3 karakter")
            self.company_name = company_name

        if industry is not None:
            self.industry = industry

        if website_url is not None:
            if not (
                website_url.startswith("http://") or website_url.startswith("https://")
            ):
                raise ValueError("URL website harus valid (http:// atau https://)")
            self.website_url = website_url

        if address is not None:
            self.address = address

        self.updated_at = datetime.utcnow()

    def can_post_vacancy(self) -> bool:
        """Cek apakah perusahaan bisa membuat lowongan

        Kriteria:
        - Harus sudah terverifikasi
        """
        return self.is_verified
