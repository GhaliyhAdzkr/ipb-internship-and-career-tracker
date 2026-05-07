import uuid
from datetime import datetime, timezone
from typing import List, Protocol

from app_backend.models.master_departments import MasterDepartments
from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.models.master_skills import MasterSkills
from app_backend.repositories.company_repository import CompanyRepository
from app_backend.repositories.department_repository import DepartmentRepository
from app_backend.repositories.skill_repository import SkillRepository
from app_backend.schemas.admin import CompanyCreate, CompanyUpdate, DepartmentCreate, DepartmentUpdate, SkillCreate, SkillUpdate


class IMasterDataService(Protocol):
    def list_departments(self) -> List[MasterDepartments]: ...
    def create_department(self, data: DepartmentCreate) -> MasterDepartments: ...
    def update_department(self, dept_id: uuid.UUID, data: DepartmentUpdate) -> MasterDepartments: ...
    def delete_department(self, dept_id: uuid.UUID) -> None: ...

    def list_skills(self) -> List[MasterSkills]: ...
    def create_skill(self, data: SkillCreate) -> MasterSkills: ...
    def update_skill(self, skill_id: uuid.UUID, data: SkillUpdate) -> MasterSkills: ...
    def delete_skill(self, skill_id: uuid.UUID) -> None: ...

    def list_companies(self) -> List[MasterExternalCompanies]: ...
    def create_company(self, data: CompanyCreate) -> MasterExternalCompanies: ...
    def update_company(self, company_id: uuid.UUID, data: CompanyUpdate) -> MasterExternalCompanies: ...
    def delete_company(self, company_id: uuid.UUID) -> None: ...


class MasterDataService:
    def __init__(
        self,
        department_repo: DepartmentRepository,
        skill_repo: SkillRepository,
        company_repo: CompanyRepository,
    ):
        self.department_repo = department_repo
        self.skill_repo = skill_repo
        self.company_repo = company_repo

    def list_departments(self, skip: int = 0, limit: int = 100) -> List[MasterDepartments]:
        return self.department_repo.get_all(skip, limit)

    def create_department(self, data: DepartmentCreate) -> MasterDepartments:
        department = MasterDepartments(id=uuid.uuid4(), code=data.code, name=data.name, faculty=data.faculty)
        self.department_repo.create(department)
        self.department_repo.save_changes()
        return department

    def update_department(self, dept_id: uuid.UUID, data: DepartmentUpdate) -> MasterDepartments:
        dept = self.department_repo.get_by_id(dept_id)
        if not dept:
            raise ValueError("Prodi tidak ditemukan")
        if data.code is not None:
            dept.code = data.code
        if data.name is not None:
            dept.name = data.name
        if data.faculty is not None:
            dept.faculty = data.faculty
        self.department_repo.save_changes()
        return dept

    def delete_department(self, dept_id: uuid.UUID) -> None:
        dept = self.department_repo.get_by_id(dept_id)
        if not dept:
            raise ValueError("Prodi tidak ditemukan")
        self.department_repo.delete(dept)
        self.department_repo.save_changes()

    def list_skills(self, skip: int = 0, limit: int = 100) -> List[MasterSkills]:
        return self.skill_repo.get_all(skip, limit)

    def create_skill(self, data: SkillCreate) -> MasterSkills:
        skill = MasterSkills(id=uuid.uuid4(), name=data.name, category=data.category)
        self.skill_repo.create(skill)
        self.skill_repo.save_changes()
        return skill

    def update_skill(self, skill_id: uuid.UUID, data: SkillUpdate) -> MasterSkills:
        skill = self.skill_repo.get_by_id(skill_id)
        if not skill:
            raise ValueError("Skill tidak ditemukan")
        if data.name is not None:
            skill.name = data.name
        if data.category is not None:
            skill.category = data.category
        self.skill_repo.save_changes()
        return skill

    def delete_skill(self, skill_id: uuid.UUID) -> None:
        skill = self.skill_repo.get_by_id(skill_id)
        if not skill:
            raise ValueError("Skill tidak ditemukan")
        self.skill_repo.delete(skill)
        self.skill_repo.save_changes()

    def list_companies(self, skip: int = 0, limit: int = 100) -> List[MasterExternalCompanies]:
        return self.company_repo.get_all(skip, limit)

    def create_company(self, data: CompanyCreate) -> MasterExternalCompanies:
        company = MasterExternalCompanies(
            id=uuid.uuid4(),
            name=data.name,
            industry=data.industry,
            website_url=str(data.website_url) if data.website_url else None,
            address=data.address,
            created_at=datetime.now(timezone.utc),
        )
        self.company_repo.create(company)
        self.company_repo.save_changes()
        return company

    def update_company(self, company_id: uuid.UUID, data: CompanyUpdate) -> MasterExternalCompanies:
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise ValueError("Perusahaan tidak ditemukan")
        if data.name is not None:
            company.name = data.name
        if data.industry is not None:
            company.industry = data.industry
        if data.website_url is not None:
            company.website_url = str(data.website_url)
        if data.address is not None:
            company.address = data.address
        self.company_repo.save_changes()
        return company

    def delete_company(self, company_id: uuid.UUID) -> None:
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise ValueError("Perusahaan tidak ditemukan")
        self.company_repo.delete(company)
        self.company_repo.save_changes()
