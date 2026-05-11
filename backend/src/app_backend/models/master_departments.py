"""
Model: public.master_departments
Tabel master untuk Program Studi dan Fakultas.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.profiles_student import ProfilesStudent


class MasterDepartments(Base):
    __tablename__ = "master_departments"
    __table_args__ = (UniqueConstraint("code", name="master_departments_code_key"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    faculty: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    profiles_student: Mapped[list["ProfilesStudent"]] = relationship("ProfilesStudent", back_populates="department")
