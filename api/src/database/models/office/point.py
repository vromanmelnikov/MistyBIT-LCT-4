from sqlalchemy import JSON, Boolean, Integer, String, Column, Date, Text
from datetime import date

from src.database.base import Base


class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    created_at = Column(Date, default=date.today, comment="Дата создания")
    img = Column(Text, nullable=True)
    coordinate = Column(JSON)
    is_delivered_card = Column(Boolean, default=False, comment="Карты были доставлены?")
    last_date_issue_card = Column(Date, comment="Последняя дата выдачи карт")
    quantity_requests = Column(Integer, comment="Количество заявок")
    quantity_card = Column(Integer, comment="Количество выданных карт")
