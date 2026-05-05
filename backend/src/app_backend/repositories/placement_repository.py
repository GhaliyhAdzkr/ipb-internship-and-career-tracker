from sqlalchemy.orm import Session

from app_backend.models.placements import Placements
from app_backend.repositories.base import BaseRepository


class PlacementRepository(BaseRepository[Placements]):
    def __init__(self, session: Session):
        super().__init__(Placements, session)
