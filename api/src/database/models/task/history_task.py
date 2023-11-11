from sqlalchemy import JSON, DateTime, ForeignKey, Integer, Column, Text
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.database.models.task.task_status import TaskStatus


class HistoryTask(Base):
    __tablename__ = "history_tasks"
    id = Column(Integer, primary_key=True)
    type = Column(JSON)
    type_id = Column(Integer)
    point = Column(JSON)
    point_id = Column(Integer)
    status_id = Column(Integer, ForeignKey(TaskStatus.id))
    employee = Column(JSON)
    employee_id = Column(Integer)
    feedback_value=Column(Integer)
    feedback_description=Column(Text)
    

    date_begin = Column(DateTime, nullable=True)
    date_create = Column(DateTime, nullable=True)

    status = relationship(TaskStatus, backref="history_tasks")
