from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Column, Text
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.models.users.user import User


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    date_create = Column(DateTime, default=datetime.utcnow)
    

    user = relationship(User, backref="notes")
