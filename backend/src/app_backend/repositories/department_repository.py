from sqlalchemy.orm import Session

from app_backend.models.master_departments import MasterDepartments
from app_backend.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[MasterDepartments]):
    def __init__(self, session: Session):
        super().__init__(MasterDepartments, session)
