"""
Manage External Companies Feature – Command Handlers.
CRUD lengkap untuk tabel public.master_external_companies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.schemas.admin import CompanyCreate, CompanyResponse, CompanyUpdate


@dataclass
class ListCompaniesCommand:
    pass


@dataclass
class ListCompaniesResult:
    items: list[CompanyResponse]
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_companies_command_handler(
    command: ListCompaniesCommand,
    session: Session,
) -> ListCompaniesResult:
    rows = session.query(MasterExternalCompanies).order_by(MasterExternalCompanies.name).all()
    return ListCompaniesResult(items=[CompanyResponse.model_validate(r) for r in rows])


@dataclass
class CreateCompanyCommand:
    payload: CompanyCreate


@dataclass
class CreateCompanyResult:
    item: Optional[CompanyResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def create_company_command_handler(
    command: CreateCompanyCommand,
    session: Session,
) -> CreateCompanyResult:
    try:
        company = MasterExternalCompanies(
            id=uuid.uuid4(),
            name=command.payload.name,
            industry=command.payload.industry,
            website_url=command.payload.website_url,
            address=command.payload.address,
            created_at=datetime.now(timezone.utc),
        )
        session.add(company)
        session.commit()
        session.refresh(company)
        return CreateCompanyResult(item=CompanyResponse.model_validate(company))
    except IntegrityError:
        session.rollback()
        return CreateCompanyResult(error_message=f"Perusahaan '{command.payload.name}' sudah ada")
    except Exception as exc:
        session.rollback()
        return CreateCompanyResult(error_message=f"Gagal membuat perusahaan: {exc}")


@dataclass
class UpdateCompanyCommand:
    company_id: uuid.UUID
    payload: CompanyUpdate


@dataclass
class UpdateCompanyResult:
    item: Optional[CompanyResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def update_company_command_handler(
    command: UpdateCompanyCommand,
    session: Session,
) -> UpdateCompanyResult:
    company = session.query(MasterExternalCompanies).filter(MasterExternalCompanies.id == command.company_id).first()
    if not company:
        return UpdateCompanyResult(error_message="Perusahaan tidak ditemukan")

    try:
        if command.payload.name is not None:
            company.name = command.payload.name
        if command.payload.industry is not None:
            company.industry = command.payload.industry
        if command.payload.website_url is not None:
            company.website_url = command.payload.website_url
        if command.payload.address is not None:
            company.address = command.payload.address
        session.commit()
        session.refresh(company)
        return UpdateCompanyResult(item=CompanyResponse.model_validate(company))
    except IntegrityError:
        session.rollback()
        return UpdateCompanyResult(error_message=f"Nama perusahaan '{command.payload.name}' sudah digunakan")
    except Exception as exc:
        session.rollback()
        return UpdateCompanyResult(error_message=f"Gagal update perusahaan: {exc}")


@dataclass
class DeleteCompanyCommand:
    company_id: uuid.UUID


@dataclass
class DeleteCompanyResult:
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def delete_company_command_handler(
    command: DeleteCompanyCommand,
    session: Session,
) -> DeleteCompanyResult:
    company = session.query(MasterExternalCompanies).filter(MasterExternalCompanies.id == command.company_id).first()
    if not company:
        return DeleteCompanyResult(error_message="Perusahaan tidak ditemukan")

    try:
        session.delete(company)
        session.commit()
        return DeleteCompanyResult()
    except IntegrityError:
        session.rollback()
        return DeleteCompanyResult(
            error_message="Tidak dapat menghapus perusahaan yang masih direferensikan oleh lowongan atau penempatan"
        )
    except Exception as exc:
        session.rollback()
        return DeleteCompanyResult(error_message=f"Gagal menghapus perusahaan: {exc}")
