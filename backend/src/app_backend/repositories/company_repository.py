from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[MasterExternalCompanies]):
    def __init__(self, session: Session):
        super().__init__(MasterExternalCompanies, session)

    def get_distinct_industries(self) -> List[str]:
        query = select(MasterExternalCompanies.industry).distinct().where(MasterExternalCompanies.industry.is_not(None))
        return list(self.session.scalars(query).all())
