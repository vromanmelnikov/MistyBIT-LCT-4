from enum import Enum
from pydantic import BaseModel, Field, conlist
from datetime import date


class SubjectData(BaseModel):
    id: int
    role_id: int


class ResourceData(BaseModel):
    name: str
    id: int | str | None = None
    owner_id: int | None = None
    details: dict | None = None


class ActionData(BaseModel):
    name: str


class StatusAccess(Enum):
    allow = True
    denied = False


class UpdateUserData(BaseModel):
    lastname: str = Field(min_length=1, max_length=100)
    firstname: str = Field(min_length=1, max_length=100)
    patronymic: str = Field(min_length=1, max_length=100)
    birthdate: date | None = None
    gender: bool | None = None
    image: str | None = None


class SubjectPolicySchema(BaseModel):
    role_id: int
    is_owner: bool | None = False


class UpdatePolicySchema(BaseModel):
    uid: int
    description: str
    subjects: conlist(SubjectPolicySchema, min_length=1)
