import uuid
from datetime import datetime, timezone
from typing import List, Optional, Protocol

from app_backend.models.vacancies import Vacancies
from app_backend.models.vacancy_skills import VacancySkills
from app_backend.repositories.company_repository import CompanyRepository
from app_backend.repositories.vacancy_repository import VacancyRepository
from app_backend.repositories.vacancy_skill_repository import VacancySkillRepository
from app_backend.schemas.vacancy import CompanyInfo, VacancyCreate, VacancyDetailResponse, VacancyResponse, VacancyUpdate


class IVacancyService(Protocol):
    def create_vacancy(self, data: VacancyCreate, created_by: uuid.UUID) -> VacancyResponse: ...
    def get_vacancy(self, vacancy_id: uuid.UUID) -> Optional[VacancyDetailResponse]: ...
    def update_vacancy(self, vacancy_id: uuid.UUID, data: VacancyUpdate) -> VacancyResponse: ...
    def delete_vacancy(self, vacancy_id: uuid.UUID) -> None: ...
    def list_active_vacancies(self, skip: int = 0, limit: int = 100) -> List[VacancyDetailResponse]: ...


class VacancyService:
    def __init__(
        self,
        vacancy_repo: VacancyRepository,
        vacancy_skill_repo: VacancySkillRepository,
        company_repo: CompanyRepository,
    ):
        self.vacancy_repo = vacancy_repo
        self.vacancy_skill_repo = vacancy_skill_repo
        self.company_repo = company_repo

    def create_vacancy(self, data: VacancyCreate, created_by: Optional[uuid.UUID] = None) -> VacancyResponse:
        if not self.company_repo.get_by_id(data.company_id):
            raise ValueError("Perusahaan tidak ditemukan")
        if data.close_date <= data.open_date:
            raise ValueError("Tanggal tutup harus setelah tanggal buka")
        if data.compensation_min and data.compensation_max:
            if data.compensation_min > data.compensation_max:
                raise ValueError("Kompensasi minimum tidak boleh lebih besar dari maksimum")

        try:
            now = datetime.now(timezone.utc)
            vacancy = Vacancies(
                id=uuid.uuid4(),
                company_id=data.company_id,
                title=data.title,
                description=data.description,
                type=data.type.value,
                open_date=data.open_date,
                close_date=data.close_date,
                location=data.location,
                payment_type=(data.payment_type.value if data.payment_type else "UNPAID"),
                compensation_min=data.compensation_min,
                compensation_max=data.compensation_max,
                compensation_note=data.compensation_note,
                source_url=str(data.source_url) if data.source_url else None,
                is_scraped=False,
                is_auto_close=True,
                is_active=True,
                created_by=created_by,
                created_at=now,
                updated_at=now,
            )
            self.vacancy_repo.create(vacancy)
            self.vacancy_repo.flush()

            if data.skills:
                for skill_item in data.skills:
                    vacancy_skill = VacancySkills(
                        vacancy_id=vacancy.id,
                        skill_id=skill_item.skill_id,
                        is_mandatory=skill_item.is_mandatory,
                    )
                    self.vacancy_skill_repo.create(vacancy_skill)

            self.vacancy_repo.save_changes()
            return self._map_to_response(vacancy)
        except Exception as exc:
            self.vacancy_repo.rollback()
            raise exc

    def get_vacancy(self, vacancy_id: uuid.UUID) -> Optional[VacancyDetailResponse]:
        vacancy = self.vacancy_repo.get_with_company(vacancy_id)
        if not vacancy:
            return None

        # Fetch skills for detail view
        skills = self.vacancy_skill_repo.get_by_vacancy_id(vacancy_id)
        
        company_info = (
            CompanyInfo(
                id=vacancy.company.id,
                name=vacancy.company.name,
                industry=vacancy.company.industry,
                website_url=vacancy.company.website_url,
                logo_url=vacancy.company.logo_url,
            )
            if vacancy.company
            else None
        )

        return VacancyDetailResponse(
            id=vacancy.id,
            company=company_info,
            title=vacancy.title,
            description=vacancy.description,
            type=vacancy.type,
            open_date=vacancy.open_date,
            close_date=vacancy.close_date,
            location=vacancy.location,
            payment_type=vacancy.payment_type,
            compensation_min=vacancy.compensation_min,
            compensation_max=vacancy.compensation_max,
            compensation_note=vacancy.compensation_note,
            source_url=vacancy.source_url,
            is_scraped=vacancy.is_scraped if vacancy.is_scraped is not None else False,
            is_auto_close=(vacancy.is_auto_close if vacancy.is_auto_close is not None else True),
            is_active=vacancy.is_active if vacancy.is_active is not None else True,
            skills=skills,
            created_at=vacancy.created_at,
            updated_at=vacancy.updated_at,
        )

    def update_vacancy(self, vacancy_id: uuid.UUID, data: VacancyUpdate) -> VacancyResponse:
        vacancy = self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise ValueError("Lowongan tidak ditemukan")

        if data.title is not None:
            vacancy.title = data.title
        if data.description is not None:
            vacancy.description = data.description
        if data.location is not None:
            vacancy.location = data.location
        if data.type is not None:
            vacancy.type = data.type.value
        if data.payment_type is not None:
            vacancy.payment_type = data.payment_type.value
        if data.open_date is not None:
            vacancy.open_date = data.open_date
        if data.close_date is not None:
            vacancy.close_date = data.close_date
        if data.compensation_min is not None:
            vacancy.compensation_min = data.compensation_min
        if data.compensation_max is not None:
            vacancy.compensation_max = data.compensation_max
        if data.compensation_note is not None:
            vacancy.compensation_note = data.compensation_note
        if data.source_url is not None:
            vacancy.source_url = str(data.source_url)
        if data.is_active is not None:
            vacancy.is_active = data.is_active

        vacancy.updated_at = datetime.now(timezone.utc)
        self.vacancy_repo.save_changes()
        return self._map_to_response(vacancy)

    def delete_vacancy(self, vacancy_id: uuid.UUID) -> None:
        vacancy = self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise ValueError("Lowongan tidak ditemukan")

        # Soft delete
        vacancy.is_active = False
        vacancy.updated_at = datetime.now(timezone.utc)
        self.vacancy_repo.save_changes()

    def list_active_vacancies(self, skip: int = 0, limit: int = 100) -> List[VacancyDetailResponse]:
        vacancies = self.vacancy_repo.list_active(skip, limit)
        return [self._map_to_detail_response(v) for v in vacancies]

    def count_active_vacancies(self) -> int:
        return self.vacancy_repo.count_active()

    def list_industries(self) -> List[str]:
        return self.company_repo.get_distinct_industries()

    def _map_to_response(self, vacancy: Vacancies) -> VacancyResponse:
        return VacancyResponse(
            id=vacancy.id,
            company_id=vacancy.company_id,
            title=vacancy.title,
            description=vacancy.description,
            type=vacancy.type,
            open_date=vacancy.open_date,
            close_date=vacancy.close_date,
            location=vacancy.location,
            payment_type=vacancy.payment_type,
            compensation_min=vacancy.compensation_min,
            compensation_max=vacancy.compensation_max,
            compensation_note=vacancy.compensation_note,
            source_url=vacancy.source_url,
            is_scraped=vacancy.is_scraped if vacancy.is_scraped is not None else False,
            is_auto_close=(vacancy.is_auto_close if vacancy.is_auto_close is not None else True),
            is_active=vacancy.is_active if vacancy.is_active is not None else True,
            created_at=vacancy.created_at,
            updated_at=vacancy.updated_at,
        )

    def _map_to_detail_response(self, vacancy: Vacancies) -> VacancyDetailResponse:
        company_info = None
        if vacancy.company:
            company_info = CompanyInfo(
                id=vacancy.company.id,
                name=vacancy.company.name,
                industry=vacancy.company.industry,
                website_url=vacancy.company.website_url,
                logo_url=vacancy.company.logo_url,
            )
        elif vacancy.company_id:
            company = self.company_repo.get_by_id(vacancy.company_id)
            if company:
                company_info = CompanyInfo(
                    id=company.id,
                    name=company.name,
                    industry=company.industry,
                    website_url=company.website_url,
                    logo_url=company.logo_url,
                )

        return VacancyDetailResponse(
            id=vacancy.id,
            company=company_info,
            title=vacancy.title,
            description=vacancy.description,
            type=vacancy.type,
            open_date=vacancy.open_date,
            close_date=vacancy.close_date,
            location=vacancy.location,
            payment_type=vacancy.payment_type,
            compensation_min=vacancy.compensation_min,
            compensation_max=vacancy.compensation_max,
            compensation_note=vacancy.compensation_note,
            source_url=vacancy.source_url,
            is_scraped=vacancy.is_scraped if vacancy.is_scraped is not None else False,
            is_auto_close=(vacancy.is_auto_close if vacancy.is_auto_close is not None else True),
            is_active=vacancy.is_active if vacancy.is_active is not None else True,
            skills=[],  # Skills empty for list view to save bandwidth
            created_at=vacancy.created_at,
            updated_at=vacancy.updated_at,
        )
