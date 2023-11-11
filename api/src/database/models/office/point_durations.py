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
from src.database.models.office.point import Point


class PointDuration(Base):
    __tablename__ = "point_durations"
    id = Column(Integer, primary_key=True)
    point_id1 = Column(Integer, ForeignKey("points.id"))
    point_id2 = Column(Integer, ForeignKey("points.id"))
    value = Column(Integer)

    point1 = relationship(Point, foreign_keys=point_id1, backref="point_durations1")
    point2 = relationship(Point, foreign_keys=point_id2, backref="point_durations2")
