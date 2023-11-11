from sqlalchemy import Integer, String, Column

from src.database.base import Base


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    value = Column(Integer)