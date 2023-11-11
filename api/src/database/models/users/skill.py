from sqlalchemy import Integer, String, Column

from src.database.base import Base


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
