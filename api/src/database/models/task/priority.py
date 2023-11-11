from sqlalchemy import Integer, String, Column

from src.database.base import Base


class Priority(Base):
    __tablename__ = "priorities"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)
