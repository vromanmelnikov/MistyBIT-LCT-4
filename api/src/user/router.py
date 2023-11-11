from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from src.authorization.schemas import ResourceData
from src.background_tasks.mail import send_greeting

from src.authorization.authorization import AuthorizationService
from src.authorization.dependies import factory_default_auth
from src.user.dependies import factory_user_auth
from src.config import OAuth2Scheme
from src.const import *
from src.schemas.response_items import ResponseItemsSchema
from src.user.const import *
from src.user.dependies import create_user_service
from src.user.service import UserService
from src.user.schemas import *

router = APIRouter(prefix=COMMON_URL, tags=["Users"])


@router.get(
    "/grades/all",
    response_model=ResponseItemsSchema[GradeSchema],
    summary="Получение всех грейдов",
)
async def get_operators(
    user_service: UserService = Depends(create_user_service),
):
    return await user_service.get_all_grades()


@router.get(
    f"{ROLES}{ALL}",
    response_model=ResponseItemsSchema[RoleSchema],
    summary="Получение всех ролей",
)
async def get_roles(
    is_all: bool = True,
    user_service: UserService = Depends(create_user_service),
):
    return await user_service.get_all_roles(is_all)


@router.get(
    PROFILE,
    response_model=FullUserSchema,
    summary=f"Получение профиля {SUPPORT_SECURITY_OWNER}",
)
async def get_by_id_profile(
    request: Request,
    token: str = Depends(OAuth2Scheme),
    id: int = Query(default=None),
    authorization_service: AuthorizationService = Depends(factory_user_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=id), token
    )
    user_id = id if id else subject_data.id
    return await user_service.get_profile(user_id)


@router.post(REGISTRATION, summary="Регистрация пользователей")
async def add_profile(
    request: Request,
    user: CreateUserSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    user_service: UserService = Depends(create_user_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    msg, email, url, firstname = await user_service.registration(user)
    send_greeting.delay(email, url, firstname)
    return msg


@router.get(
    f"{SKILLS}{ALL}",
    response_model=ResponseItemsSchema[SkillSchema],
    summary="Получение всех навыков",
)
async def get_skills(user_service: UserService = Depends(create_user_service)):
    return await user_service.get_skills()


@router.post(SKILLS, summary="Добавление навыка")
async def add_skill(
    request: Request,
    skill: SkillPostSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.post_skill(skill)


@router.post(f"{SKILLS}{EMPLOYEE}", summary="Добавление навыка сотруднику")
async def add_skill_employee(
    request: Request,
    skill_employee: SkillEmployeePostSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.post_skill_employee(subject_data.id, skill_employee)


@router.delete(f"{SKILLS}{EMPLOYEE}", summary="Удаление навыка сотруднику")
async def delete_skill_employee(
    request: Request,
    id: int,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.delete_skill_employee(subject_data.id, id)


@router.get(
    ALL,
    response_model=ResponseItemsSchema[UserFullGetSchema],
    summary="Вывод всех пользователей",
)
async def get_users(
    request: Request,
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво пользователей",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    role_id: int = Query(default=None, description="ИД роли"),
    substr: str = Query(default=None, description="Подстрока фамилии пользователя"),
    user_service: UserService = Depends(create_user_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.get_users(limit, offset, substr, role_id)


@router.get(f"{EMPLOYEES}{ALL}", summary="Получение сотрудников")
async def get_employees(
    request: Request,
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво пользователей",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    substr: str = Query(default=None, description="Подстрока фамилии сотрудника"),
    office_id: int = Query(default=None, description="ИД офиса"),
    user_service: UserService = Depends(create_user_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.get_employees(limit, offset, substr, office_id)


@router.put(EMPLOYEES, summary=f"Изменение сотрудника {SUPPORT_SECURITY_OWNER}")
async def update_employee(
    request: Request,
    employee: EmployeePutSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_user_auth),
    user_service: UserService = Depends(create_user_service),
):
    await authorization_service.check_authorization(
        request.method.lower(),
        ResourceData(name=request.url.path, id=employee.id),
        token,
    )
    return await user_service.put_employees(employee)


@router.put("/", summary=f"Изменение пользователя (фио) {SUPPORT_SECURITY_OWNER}")
async def put_user(
    request: Request,
    user: UserPutSchema,
    id: int = Query(default=None, description="Если id не указан то меняется сам себя"),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_user_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=id), token
    )
    user_id = id if id else subject_data.id
    return await user_service.put_user(user_id, user)


@router.delete("/", summary=f"Удаление пользователя {SUPPORT_SECURITY_OWNER}")
async def delete_profile(
    request: Request,
    id: int = Query(default=None, description="Если id не указан то удаляет сам себя"),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_user_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=id), token
    )
    user_id = id if id else subject_data.id
    return await user_service.delete_user(user_id)


@router.delete(IMMAGE, summary="Удаление картинки пользователя")
async def delete_image_user(
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.delete_image_user(subject_data.id)


@router.post(IMMAGE, summary="Изменение картинки пользователя")
async def post_user_image(
    request: Request,
    file: UploadFile = File(...),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await user_service.post_image_user(subject_data.id, file)


@router.put(
    IS_ACTIVE,
    summary=f"Изменение статуса сотрудника (актив/неактив) {SUPPORT_SECURITY_OWNER}",
)
async def put_user_active(
    request: Request,
    user_id: int,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_user_auth),
    user_service: UserService = Depends(create_user_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=user_id), token
    )
    return await user_service.put_user_active(user_id)
