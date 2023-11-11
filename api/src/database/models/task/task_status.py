from sqlalchemy import Boolean, Integer, String, Column

from src.database.base import Base


class TaskStatus(Base):
    __tablename__ = "task_statusess"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    in_history = Column(Boolean, default=False)
