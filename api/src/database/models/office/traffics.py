from sqlalchemy import JSON, Boolean, Integer, String, Column, DateTime, Text
from datetime import datetime

from src.database.base import Base


class Traffic(Base):
    __tablename__ = "traffics"
    id = Column(Integer, primary_key=True)
    hour = Column(Integer)
    level = Column(Integer)
