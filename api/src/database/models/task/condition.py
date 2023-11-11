from sqlalchemy import JSON, ForeignKey, Integer, Column, Text
from sqlalchemy.orm import relationship

from src.database.models.task.type_task import TypeTask
from src.database.base import Base
from sqlalchemy.orm import backref


class Condition(Base):
    __tablename__ = "conditions"
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    formula = Column(JSON)
    type_task_id = Column(Integer, ForeignKey(TypeTask.id))

    type_task = relationship(TypeTask, backref=backref("conditions", cascade="all, delete"))