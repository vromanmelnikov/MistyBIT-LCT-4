from sqlalchemy import Integer, Column, ForeignKey

from src.database.base import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

