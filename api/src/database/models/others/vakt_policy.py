from sqlalchemy import JSON, Integer, Column, Text

from src.database.base import Base


class VaktPolicy(Base):
    __tablename__ = "vakt_policies"
    id = Column(Integer, primary_key=True)
    resources = Column(JSON)
    actions = Column(JSON)
    subjects = Column(JSON)
    description = Column(Text)
