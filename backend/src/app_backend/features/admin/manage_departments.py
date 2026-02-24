"""
Manage Departments Feature – Command Handlers.
CRUD lengkap untuk tabel public.master_departments.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app_backend.models.master_departments import MasterDepartments
from app_backend.schemas.admin import (DepartmentCreate, DepartmentResponse,
                                       DepartmentUpdate)

# ─── List ────────────────────────────────────────────────────────────────────


@dataclass
class ListDepartmentsCommand:
    pass


@dataclass
class ListDepartmentsResult:
    items: list[DepartmentResponse]
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_departments_command_handler(
    command: ListDepartmentsCommand,
    session: Session,
) -> ListDepartmentsResult:
    rows = session.query(MasterDepartments).order_by(MasterDepartments.name).all()
    return ListDepartmentsResult(
        items=[DepartmentResponse.model_validate(r) for r in rows]
    )


# ─── Create ──────────────────────────────────────────────────────────────────


@dataclass
class CreateDepartmentCommand:
    payload: DepartmentCreate


@dataclass
class CreateDepartmentResult:
    item: Optional[DepartmentResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def create_department_command_handler(
    command: CreateDepartmentCommand,
    session: Session,
) -> CreateDepartmentResult:
    try:
        dept = MasterDepartments(
            id=uuid.uuid4(),
            code=command.payload.code.upper(),
            name=command.payload.name,
            faculty=command.payload.faculty,
        )
        session.add(dept)
        session.commit()
        session.refresh(dept)
        return CreateDepartmentResult(item=DepartmentResponse.model_validate(dept))
    except IntegrityError:
        session.rollback()
        return CreateDepartmentResult(
            error_message=f"Kode '{command.payload.code}' sudah ada"
        )
    except Exception as exc:
        session.rollback()
        return CreateDepartmentResult(error_message=f"Gagal membuat departemen: {exc}")


# ─── Update ──────────────────────────────────────────────────────────────────


@dataclass
class UpdateDepartmentCommand:
    dept_id: uuid.UUID
    payload: DepartmentUpdate


@dataclass
class UpdateDepartmentResult:
    item: Optional[DepartmentResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def update_department_command_handler(
    command: UpdateDepartmentCommand,
    session: Session,
) -> UpdateDepartmentResult:
    dept = (
        session.query(MasterDepartments)
        .filter(MasterDepartments.id == command.dept_id)
        .first()
    )
    if not dept:
        return UpdateDepartmentResult(error_message="Departemen tidak ditemukan")

    try:
        if command.payload.code is not None:
            dept.code = command.payload.code.upper()
        if command.payload.name is not None:
            dept.name = command.payload.name
        if command.payload.faculty is not None:
            dept.faculty = command.payload.faculty
        session.commit()
        session.refresh(dept)
        return UpdateDepartmentResult(item=DepartmentResponse.model_validate(dept))
    except IntegrityError:
        session.rollback()
        return UpdateDepartmentResult(
            error_message=f"Kode '{command.payload.code}' sudah digunakan"
        )
    except Exception as exc:
        session.rollback()
        return UpdateDepartmentResult(error_message=f"Gagal update departemen: {exc}")


# ─── Delete ──────────────────────────────────────────────────────────────────


@dataclass
class DeleteDepartmentCommand:
    dept_id: uuid.UUID


@dataclass
class DeleteDepartmentResult:
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def delete_department_command_handler(
    command: DeleteDepartmentCommand,
    session: Session,
) -> DeleteDepartmentResult:
    dept = (
        session.query(MasterDepartments)
        .filter(MasterDepartments.id == command.dept_id)
        .first()
    )
    if not dept:
        return DeleteDepartmentResult(error_message="Departemen tidak ditemukan")

    try:
        session.delete(dept)
        session.commit()
        return DeleteDepartmentResult()
    except IntegrityError:
        session.rollback()
        return DeleteDepartmentResult(
            error_message="Tidak dapat menghapus departemen yang masih dipakai oleh profil mahasiswa"
        )
    except Exception as exc:
        session.rollback()
        return DeleteDepartmentResult(
            error_message=f"Gagal menghapus departemen: {exc}"
        )
