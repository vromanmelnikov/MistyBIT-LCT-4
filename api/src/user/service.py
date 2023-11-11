import secrets
from fastapi import UploadFile, status
import requests
from src.authentication.schemas import RecoverPasswordSchema

from src.authentication.service import AuthenticationService
from src.config import settings
from src.exceptions import AnyServiceException, BadRequestException, NotFoundException
from src.schemas.response_items import ResponseItemsSchema
from src.const import EXPIRES_WEEK_CACHE_ON_SECONDS, ROLE_EMPLOYEE
from src.user.phrases import *
from src.authentication.exceptions import *
from src.database.exceptions import *
from src.schemas.message import MessageSchema
from src.services.unit_of_work import IUnitOfWork
from src.user.exceptions import *
from src.user.schemas import *
from src.database.models import *
from src.utils import check_count_items, check_exist_items


class UserService:
    def __init__(
        self,
        uow: IUnitOfWork,
        select_user_mappers: dict[str, TypeSelectMapperSchema],
    ):
        self.__select_user_mappers = select_user_mappers
        self.__uow = uow

    async def get_all_grades(self):
        async with self.__uow:
            try:
                grades = await self.__uow.grades.get_all()
                l = check_count_items(grades, GRADES_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [GradeSchema.from_orm(g) for g in grades], None, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def get_all_roles(self, is_all: bool):
        async with self.__uow:
            try:
                kwargs = {}
                if not is_all:
                    kwargs["is_public"] = True
                roles = await self.__uow.roles.get_all(**kwargs)
                l = check_count_items(roles, ROLES_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [RoleSchema.from_orm(r) for r in roles], None, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def get_profile(self, user_id: int):
        async with self.__uow:
            try:
                user = await self.__uow.users.get_by_id(user_id)
                if user is None:
                    raise NotFoundException(INVALID_ID)
                return FullUserSchema.from_orm(user)
            except GetItemByIdException as e:
                raise AnyServiceException(GET_USER_BY_ID_EXCEPTION) from e

    async def get_skills(self) -> ResponseItemsSchema[SkillSchema]:
        async with self.__uow:
            try:
                skills = await self.__uow.skills.get_all()
                l = check_count_items(skills, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [SkillSchema.from_orm(s) for s in skills], None, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def post_skill(self, skill: SkillPostSchema):
        async with self.__uow:
            try:
                skill_db = Skill(name=skill.name)
                await self.__uow.skills.add(skill_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_ADD_SUCCESS)
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def get_users(
        self,
        limit: int | None,
        offset: int | None,
        substr: str | None,
        role_id: int | None,
    ) -> ResponseItemsSchema[UserFullGetSchema]:
        async with self.__uow:
            try:
                users = await self.__uow.users.get_all_full(
                    limit, offset, substr, role_id
                )
                l = check_count_items(users, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [UserFullGetSchema.from_orm(u) for u in users], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def get_employees(
        self,
        limit: int | None,
        offset: int | None,
        substr: str | None,
        office_id: int | None,
    ) -> ResponseItemsSchema[EmployeeFullGetSchema]:
        async with self.__uow:
            try:
                employees = await self.__uow.employees.get_all_full(
                    limit, offset, substr, office_id, None
                )
                l = check_count_items(employees, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [EmployeeFullGetSchema.from_orm(e) for e in employees], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def registration(self, user: CreateUserSchema):
        async with self.__uow:
            auth_service = AuthenticationService(self.__uow)
            await auth_service.check_exist_user(user.email, self.__uow)

            code = secrets.token_urlsafe(8)
            user.password = auth_service.get_password_hash(code)
            select_m: TypeSelectMapperSchema = self.__select_user_mappers.get(
                user.role_id, None
            )
            if select_m is None:
                raise BadRequestException(NO_MAPPER, status.HTTP_400_BAD_REQUEST)

            user_db = select_m.mapper.create_from_input(user)
            try:
                await getattr(self.__uow, select_m.repository).add(user_db)
                await self.__uow.commit()
                _, url, _ = await auth_service.recover_password(
                    RecoverPasswordSchema(email=user.email),
                    EXPIRES_WEEK_CACHE_ON_SECONDS,
                )
                return (
                    MessageSchema(message=REGISTATION_SUCCESS),
                    user.email,
                    url,
                    user.firstname,
                )
            except (UniqueViolationException, ForeignKeyViolationException) as e:
                raise BadRequestException(e.message) from e
            except (AddItemException, UpdateItemException) as e:
                raise BadRequestException(REGISTATION_FAILED) from e

    async def post_skill_employee(
        self, user_id: int, skill_employee: SkillEmployeePostSchema
    ):
        async with self.__uow:
            try:
                skill_employee_db = EmployeeSkillLink(
                    employe_id=user_id, skill_id=skill_employee.skill_id
                )
                await self.__uow.skills.add(skill_employee_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_ADD_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def delete_skill_employee(self, user_id: int, id: int):
        async with self.__uow:
            try:
                skill_employee_exist = await self.__uow.employee_skills.get_one(
                    employe_id=user_id, skill_id=id
                )
                check_exist_items(skill_employee_exist, OBJECT_NOT_FOUND)
                await self.__uow.employee_skills.delete(employe_id=user_id, skill_id=id)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def put_employees(self, employee: EmployeePutSchema):
        async with self.__uow:
            try:
                employee_db = await self.__uow.employees.get_by_id(employee.id)
                check_exist_items(employee_db, OBJECT_NOT_FOUND)
                employee_db.grade_id = employee.grade_id
                employee_db.office_id = employee.office_id
                await self.__uow.employees.add(employee_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_UPDATE_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except UpdateItemException as e:
                raise AnyServiceException(message=OBJECT_UPDATE_FAILED) from e

    async def delete_user(self, user_id: int):
        async with self.__uow:
            try:
                user_exist = await self.__uow.users.get_by_id(user_id)
                check_exist_items(user_exist, OBJECT_NOT_FOUND)
                await self.__uow.users.delete(id=user_id)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def put_user(self, id: int, user: UserPutSchema):
        async with self.__uow:
            try:
                # if subject_data.role_id != ROLE_EMPLOYEE:
                # raise AnyServiceException()
                # else:
                # if id:
                user_db = await self.__uow.users.get_by_id(id)
                # if id is None:
                # user_db = await self.__uow.users.get_by_id(subject_data.id)
                check_exist_items(user_db, OBJECT_NOT_FOUND)
                user_db.firstname = user.firstname
                user_db.lastname = user.lastname
                user_db.patronymic = user.patronymic
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_UPDATE_SUCCESS)
            except UpdateItemException as e:
                raise AnyServiceException(message=OBJECT_UPDATE_FAILED) from e

    async def post_image_user(self, user_id: int, file: UploadFile):
        async with self.__uow:
            try:
                files = {"file": (file.filename, file.file, file.content_type)}
                res = requests.post(f"{settings.URL_UPLOAD_FILE}/", files=files)
                r = res.json()
                if res.status_code != 200:
                    raise BadRequestException(r)
                user_db = await self.__uow.users.get_by_id(user_id)
                if user_db.img is not None:
                    requests.delete(
                        f"{settings.URL_UPLOAD_FILE}/?filename={user_db.img}"
                    )
                user_db.img = r
                await self.__uow.commit()
                return r
            except Exception as e:
                AnyServiceException()

    async def delete_image_user(self, user_id: int):
        async with self.__uow:
            try:
                user_db = await self.__uow.users.get_by_id(user_id)
                res = requests.delete(
                    f"{settings.URL_UPLOAD_FILE}/?filename={user_db.img}"
                )
                r = res.json()
                if res.status_code != 200:
                    raise BadRequestException(r)
                user_db.img = None
                await self.__uow.commit()
                return MessageSchema(message=IMG_USER_DELETED)
            except Exception as e:
                AnyServiceException()

    async def put_user_active(self, user_id: int):
        async with self.__uow:
            try:
                user_db = await self.__uow.users.get_by_id(user_id)
                check_exist_items(user_db, OBJECT_NOT_FOUND)
                if user_db.is_active == False:
                    user_db.is_active = True
                else:
                    user_db.is_active = False
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_UPDATE_SUCCESS)
            except UpdateItemException as e:
                raise AnyServiceException(message=OBJECT_UPDATE_FAILED) from e
