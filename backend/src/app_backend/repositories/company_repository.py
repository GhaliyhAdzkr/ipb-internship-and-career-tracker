from sqlalchemy.orm import Session

from app_backend.models.master_external_companies import MasterExternalCompanies
from app_backend.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[MasterExternalCompanies]):
    def __init__(self, session: Session):
        super().__init__(MasterExternalCompanies, session)
