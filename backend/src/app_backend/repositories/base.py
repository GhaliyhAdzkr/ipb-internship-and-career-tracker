from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: Any) -> Optional[T]:
        return self.session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        query = select(self.model).offset(skip).limit(limit)
        return list(self.session.scalars(query).all())

    def create(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def update(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def save_changes(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def flush(self) -> None:
        self.session.flush()
