"""
Manage Skills Feature – Command Handlers.
CRUD lengkap untuk tabel public.master_skills.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app_backend.models.master_skills import MasterSkills
from app_backend.schemas.admin import SkillCreate, SkillResponse, SkillUpdate


@dataclass
class ListSkillsCommand:
    pass


@dataclass
class ListSkillsResult:
    items: list[SkillResponse]
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def list_skills_command_handler(
    command: ListSkillsCommand,
    session: Session,
) -> ListSkillsResult:
    rows = session.query(MasterSkills).order_by(MasterSkills.category, MasterSkills.name).all()
    return ListSkillsResult(items=[SkillResponse.model_validate(r) for r in rows])


@dataclass
class CreateSkillCommand:
    payload: SkillCreate


@dataclass
class CreateSkillResult:
    item: Optional[SkillResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def create_skill_command_handler(
    command: CreateSkillCommand,
    session: Session,
) -> CreateSkillResult:
    try:
        skill = MasterSkills(
            id=uuid.uuid4(),
            name=command.payload.name,
            category=command.payload.category,
        )
        session.add(skill)
        session.commit()
        session.refresh(skill)
        return CreateSkillResult(item=SkillResponse.model_validate(skill))
    except IntegrityError:
        session.rollback()
        return CreateSkillResult(error_message=f"Skill '{command.payload.name}' sudah ada")
    except Exception as exc:
        session.rollback()
        return CreateSkillResult(error_message=f"Gagal membuat skill: {exc}")


@dataclass
class UpdateSkillCommand:
    skill_id: uuid.UUID
    payload: SkillUpdate


@dataclass
class UpdateSkillResult:
    item: Optional[SkillResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def update_skill_command_handler(
    command: UpdateSkillCommand,
    session: Session,
) -> UpdateSkillResult:
    skill = session.query(MasterSkills).filter(MasterSkills.id == command.skill_id).first()
    if not skill:
        return UpdateSkillResult(error_message="Skill tidak ditemukan")

    try:
        if command.payload.name is not None:
            skill.name = command.payload.name
        if command.payload.category is not None:
            skill.category = command.payload.category
        session.commit()
        session.refresh(skill)
        return UpdateSkillResult(item=SkillResponse.model_validate(skill))
    except IntegrityError:
        session.rollback()
        return UpdateSkillResult(error_message=f"Nama skill '{command.payload.name}' sudah digunakan")
    except Exception as exc:
        session.rollback()
        return UpdateSkillResult(error_message=f"Gagal update skill: {exc}")


@dataclass
class DeleteSkillCommand:
    skill_id: uuid.UUID


@dataclass
class DeleteSkillResult:
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        return self.error_message is not None


def delete_skill_command_handler(
    command: DeleteSkillCommand,
    session: Session,
) -> DeleteSkillResult:
    skill = session.query(MasterSkills).filter(MasterSkills.id == command.skill_id).first()
    if not skill:
        return DeleteSkillResult(error_message="Skill tidak ditemukan")

    try:
        session.delete(skill)
        session.commit()
        return DeleteSkillResult()
    except IntegrityError:
        session.rollback()
        return DeleteSkillResult(error_message="Tidak dapat menghapus skill yang masih dipakai mahasiswa atau lowongan")
    except Exception as exc:
        session.rollback()
        return DeleteSkillResult(error_message=f"Gagal menghapus skill: {exc}")
