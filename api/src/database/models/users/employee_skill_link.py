from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.models.users.skill import Skill
from src.database.models.users.employee import Employee
from sqlalchemy.orm import backref


class EmployeeSkillLink(Base):
    __tablename__ = "employee_skill_links"

    employe_id = Column(Integer, ForeignKey(Employee.id), primary_key=True)
    skill_id = Column(Integer, ForeignKey(Skill.id), primary_key=True)

    user = relationship(Employee, backref=backref("skill_links", cascade="all,delete"))
    skill = relationship(Skill, backref=backref("employee_links", cascade="all,delete"))
