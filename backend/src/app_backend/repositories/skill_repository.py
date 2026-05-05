from sqlalchemy.orm import Session

from app_backend.models.master_skills import MasterSkills
from app_backend.repositories.base import BaseRepository


class SkillRepository(BaseRepository[MasterSkills]):
    def __init__(self, session: Session):
        super().__init__(MasterSkills, session)
