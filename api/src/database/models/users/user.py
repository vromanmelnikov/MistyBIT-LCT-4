from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.models.users.admin import Admin
from src.database.models.users.employee import Employee
from src.database.models.users.manager import Manager
from src.const import REPOSITORY_USERS
from src.database.base import Base
from src.database.models.users.role import Role


class User(Base):
    __tablename__ = REPOSITORY_USERS
    id = Column(Integer, primary_key=True)
    email = Column(String(320), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False)

    firstname = Column(String(100), nullable=True)
    lastname = Column(String(100), nullable=True)
    patronymic = Column(String(100), nullable=True)
    img = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(Role.id))
    is_active = Column(Boolean, default=False)

    role = relationship(Role, backref="users")
    manager = relationship(Manager, backref="user", uselist=False, cascade="all,delete")
    admin = relationship(Admin, backref="user", uselist=False, cascade="all,delete")
    employee = relationship(
        Employee, backref="user", uselist=False, cascade="all,delete"
    )
