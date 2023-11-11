from sqlalchemy import JSON, Float, ForeignKey, Integer, Column, String
from sqlalchemy.orm import relationship

from src.database.models.task.priority import Priority
from src.database.base import Base


class TypeTask(Base):
    __tablename__ = "type_tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    priority_id = Column(Integer, ForeignKey(Priority.id))
    duration = Column(Float, nullable=False)
    details = Column(JSON)
    interval_block = Column(Integer, nullable=False)

    priority = relationship(Priority, backref="type_tasks")
