from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, Field, SecretStr
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from src.database.models import *
from src.mappers import BaseMapper
from src.office.schemas import OfficeSchema


class SkillSchema(sqlalchemy_to_pydantic(Skill)):
    class Config:
        from_attributes = True


class EmployeeSkillLinkShema(sqlalchemy_to_pydantic(EmployeeSkillLink)):
    skill: SkillSchema | None = None

    class Config:
        from_attributes = True


class RoleSchema(sqlalchemy_to_pydantic(Role)):
    class Config:
        from_attributes = True


class ResetEmailSchema(BaseModel):
    new_email: EmailStr


class UserDBSchema(sqlalchemy_to_pydantic(User)):
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    img: str | None = None

    class Config:
        from_attributes = True


class UserWithoutRoleNoPassword(UserDBSchema):
    hashed_password: str | SecretStr = Field(..., exclude=True)

    class Config:
        from_attributes = True
        exclude = ["hashed_password"]


class ManagerDBSchema(sqlalchemy_to_pydantic(Manager)):
    class Config:
        from_attributes = True


class ManagerSchema(ManagerDBSchema):
    user: UserDBSchema | None = None

    class Config:
        from_attributes = True


class AdminDBSchema(sqlalchemy_to_pydantic(Admin)):
    class Config:
        from_attributes = True


class GradeSchema(sqlalchemy_to_pydantic(Grade)):
    class Config:
        from_attributes = True


class EmployeeDBSchema(sqlalchemy_to_pydantic(Employee)):
    class Config:
        from_attributes = True


class UserWithoutPswdSchema(UserDBSchema):
    hashed_password: str | SecretStr = Field(..., exclude=True)

    class Config:
        from_attributes = True
        exclude = ["hashed_password"]


class EmployeeSchema(EmployeeDBSchema):
    user: UserWithoutPswdSchema | None = None
    grade: GradeSchema | None = None
    office: OfficeSchema | None = None

    class Config:
        from_attributes = True


class FullEmployeeSchema(EmployeeDBSchema):
    grade: GradeSchema | None = None
    office: OfficeSchema | None = None
    skill_links: List[EmployeeSkillLinkShema] = []

    class Config:
        from_attributes = True


class UserWithRoleSchema(UserWithoutPswdSchema):
    role: RoleSchema | None = None

    class Config:
        from_attributes = True


class FullUserSchema(UserWithRoleSchema):
    manager: ManagerDBSchema | None = None
    admin: AdminDBSchema | None = None
    employee: FullEmployeeSchema | None = None

    class Config:
        from_attributes = True


class CreateUserSchema(BaseModel):
    role_id: int
    email: EmailStr
    password: str | None = Field(default=None, min_length=8)
    firstname: str = Field(min_length=1, max_length=100)
    lastname: str | None = Field(default=None, min_length=1, max_length=100)
    patronymic: str | None = Field(default=None, min_length=1, max_length=100)
    grade_id: int | None = None
    office_id: int | None = None


class SkillPostSchema(BaseModel):
    name: str


class UserFullGetSchema(UserWithRoleSchema):
    manager: ManagerDBSchema | None = None
    admin: AdminDBSchema | None = None
    employee: EmployeeDBSchema | None = None


class EmployeeFullGetSchema(FullEmployeeSchema):
    user: UserWithoutRoleNoPassword | None = None


class TypeSelectMapperSchema:
    def __init__(self, mapper: BaseMapper, repository: str):
        self.repository = repository
        self.mapper = mapper


class SkillEmployeePostSchema(BaseModel):
    skill_id: int


class EmployeePutSchema(BaseModel):
    id: int
    grade_id: int
    office_id: int


class UserPutSchema(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
