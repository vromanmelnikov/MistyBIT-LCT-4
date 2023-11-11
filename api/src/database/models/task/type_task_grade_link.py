from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.models.task.type_task import TypeTask
from src.database.models.users.grade import Grade
from sqlalchemy.orm import backref


class TypeTaskGradeLink(Base):
    __tablename__ = "type_task_grade_links"

    type_task_id = Column(Integer, ForeignKey(TypeTask.id), primary_key=True)
    grade_id = Column(Integer, ForeignKey(Grade.id), primary_key=True)

    type_task = relationship(TypeTask,  backref=backref("grade_links", cascade="all,delete"))
    grade = relationship(Grade, backref="type_task_links")
