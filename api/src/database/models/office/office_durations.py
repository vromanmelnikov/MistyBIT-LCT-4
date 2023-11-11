from sqlalchemy import (
    JSON,
    Boolean,
    ForeignKey,
    Integer,
    String,
    Column,
    DateTime,
    Text,
)
from datetime import datetime
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.database.models.office.office import Office
from src.database.models.office.point import Point


class OfficeDuration(Base):
    __tablename__ = "office_durations"
    id = Column(Integer, primary_key=True)
    point_id = Column(Integer, ForeignKey("points.id"))
    office_id = Column(Integer, ForeignKey("offices.id"))
    value = Column(Integer)

    office = relationship(Office, backref="office_durations")
    point = relationship(Point, backref="point_durations")