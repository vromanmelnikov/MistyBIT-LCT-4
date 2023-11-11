from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship

from src.database.models.task.type_task import TypeTask
from src.database.models.task.task_status import TaskStatus
from src.database.models.office.point import Point

from src.database.base import Base
from src.database.models.users.employee import Employee
from src.database.models.task.priority import Priority
from sqlalchemy.orm import backref


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey(TypeTask.id))
    point_id = Column(Integer, ForeignKey(Point.id))
    status_id = Column(Integer, ForeignKey(TaskStatus.id))
    employee_id = Column(Integer, ForeignKey(Employee.id))
    priority_id = Column(Integer, ForeignKey(Priority.id))
    date_create = Column(DateTime, default=datetime.utcnow)
    date_begin = Column(DateTime, nullable=True)

    type = relationship(TypeTask, backref=backref("tasks", cascade="all, delete"))
    point = relationship(Point, backref="tasks")
    status = relationship(TaskStatus, backref="tasks")
    employee = relationship(Employee, backref="tasks")
    priority = relationship(Priority, backref="tasks")
