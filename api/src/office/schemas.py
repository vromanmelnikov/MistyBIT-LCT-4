from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from typing import List
from src.database.models import *
from datetime import datetime


class OfficeSchema(sqlalchemy_to_pydantic(Office)):
    img: str | None = None

    class Config:
        from_attributes = True


class OfficePostSchema(BaseModel):
    address: str


class OfficePutSchema(OfficePostSchema):
    id: int
    coordinate: dict | None = None


class PointSchema(sqlalchemy_to_pydantic(Point)):
    img: str | None = None
    last_date_issue_card: datetime | None = None

    class Config:
        from_attributes = True


class PointPostSchema(BaseModel):
    address: str


class PointPutSchema(PointPostSchema):
    id: int
    coordinate: dict | None = None


class DictPointSchema(BaseModel):
    en: str
    ru: str
