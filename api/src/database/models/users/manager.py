from sqlalchemy import Integer, Column, ForeignKey

from src.database.base import Base


class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
