from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.models.task.type_task import TypeTask
from src.database.models.users.skill import Skill
from sqlalchemy.orm import backref


class TypeTaskSkillLinks(Base):
    __tablename__ = "type_task_skill_links"

    type_task_id = Column(Integer, ForeignKey(TypeTask.id), primary_key=True)
    skill_id = Column(Integer, ForeignKey(Skill.id), primary_key=True)

    type_task = relationship(TypeTask, backref=backref("skill_links", cascade="all,delete"))
    skill = relationship(Skill, backref="type_task_links")
