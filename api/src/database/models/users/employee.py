from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from src.database.models.office.office import Office
from src.database.models.users.grade import Grade
from src.database.base import Base


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    grade_id = Column(Integer, ForeignKey(Grade.id))
    office_id = Column(Integer, ForeignKey(Office.id))

    grade = relationship(Grade, backref="employees")
    office = relationship(Office, backref="employees")
