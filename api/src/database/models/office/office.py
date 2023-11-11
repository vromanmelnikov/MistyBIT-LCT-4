from sqlalchemy import JSON, Integer, String, Column, DateTime, Text
from datetime import datetime

from src.database.base import Base


class Office(Base):
    __tablename__ = "offices"
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    img = Column(Text, nullable=True)
    coordinate = Column(JSON)
