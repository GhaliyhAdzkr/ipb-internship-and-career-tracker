from typing import List

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app_backend.models.student_skills import StudentSkills
from app_backend.repositories.base import BaseRepository


class StudentSkillRepository(BaseRepository[StudentSkills]):
    def __init__(self, session: Session):
        super().__init__(StudentSkills, session)

    def delete_all_for_student(self, student_id) -> None:
        query = delete(StudentSkills).where(StudentSkills.student_id == student_id)
        self.session.execute(query)
        self.session.flush()

    def get_by_student_id(self, student_id) -> List[StudentSkills]:
        query = select(StudentSkills).where(StudentSkills.student_id == student_id)
        return list(self.session.scalars(query).all())
