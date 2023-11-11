from fastapi import APIRouter, Depends, Query, Request
from datetime import datetime

from src.authorization.schemas import ResourceData
from src.background_tasks.mail import send_any_message
from src.schemas.response_items import ResponseItemsSchema
from src.task.const import *
from src.const import *
from src.task.dependencies import create_task_service
from src.task.schemas import *
from src.task.service import TaskService
from src.authorization.authorization import AuthorizationService
from src.config import NoteWebsockerConnection, OAuth2Scheme
from src.authorization.dependies import factory_default_auth
from src.task.dependencies import factory_task_auth
from src.ws.dependencies import create_note_service
from src.ws.service_note import NoteService


router = APIRouter(prefix=COMMON_URL, tags=["Tasks"])


@router.get("/report", summary="Получить отчет по задачам в виде excel файла")
async def get_report(
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_report()


@router.get(
    "/",
    response_model=ResponseItemsSchema[TaskGetSchema],
    summary="Получение всех задач",
)
async def get_all_tasks(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво пользователей",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    to_all: bool = Query(default=True),
    type_id: int = Query(default=None, description="Тип задачи"),
    point_id: int = Query(default=None, description="Точка"),
    status_id: int = Query(default=None, description="Статус"),
    priority_id: int = Query(default=None, description="Приоритет"),
    employee_id: int = Query(default=None, description="Сотрудник"),
    date_create: datetime = Query(default=None, description="Дата создания"),
    date_begin: datetime = Query(default=None, description="Дата взятия"),
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_all_tasks(
        limit,
        offset,
        type_id,
        point_id,
        status_id,
        priority_id,
        employee_id,
        date_create,
        date_begin,
        to_all,
    )


@router.get(
    "/history",
    response_model=ResponseItemsSchema[TaskHistorySchema],
    summary="Получение истории задач",
)
async def get_history_task(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво пользователей",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    employee_id: int = Query(default=None, description="ИД сотрудника"),
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_history_task(limit, offset, employee_id)


@router.get(
    f"{CONDITION}{OPERATORS}{ALL}",
    response_model=ResponseItemsSchema[OperatorSchema],
    summary="Получение всех операторов",
)
async def get_conditions_operators(
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_all_operators()


@router.get(
    f"{STATUSES}{ALL}",
    response_model=ResponseItemsSchema[TaskStatusSchema],
    summary="Получение всех статусов",
)
async def get_statuses(
    in_history: bool = Query(default=False),
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_all_statuses(in_history)


@router.get(
    f"{PRIORITIES}{ALL}",
    response_model=ResponseItemsSchema[PrioritySchema],
    summary="Получение всех приоритетов",
)
async def get_priorities(
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_all_priorities()


@router.get(
    f"{TYPES}",
    response_model=ResponseItemsSchema[TypeTaskGetSchema],
    summary="Получение всех типов задач",
)
async def get_all_type_tasks(
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.get_all_type_tasks()


@router.post(f"{TYPES}", summary="Добавление типа задачи")
async def post_type_task(
    task: TypeTaskPostSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.post_type_task(task)


@router.put(f"{TYPES}", summary="Изменение типа задачи")
async def put_type_task(
    task: TypeTaskPutSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.put_type_task(task)


@router.delete(f"{TYPES}", summary="Удаление типа задачи")
async def delete_type_task(
    id: int,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.delete_type_task(id)


@router.post(f"{TYPES}{GRADES}", summary="Добавление грейда типу задачи")
async def post_type_task_grade(
    task_grade: TypeTaskGradePostSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.post_type_task_grade(task_grade)


@router.delete(f"{TYPES}{GRADES}", summary="Удаление грейда типу задачи")
async def delete_type_task_grade(
    task_grade: TypeTaskGradePostSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.delete_type_task_grade(task_grade)


@router.post(f"{TYPES}{SKILLS}", summary="Добавление навыка типу задачи")
async def post_type_task_skill(
    task_skill: TypeTaskSkillPostSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.post_type_task_skill(task_skill)


@router.delete(f"{TYPES}{SKILLS}", summary="Удаление навыка типу задачи")
async def delete_type_task_skill(
    task_skill: TypeTaskSkillPostSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.delete_type_task_skill(task_skill)


@router.post(f"{CONDITION}", summary="Добавление условия задачи")
async def post_task_conditions(
    request: Request,
    data: CreateConditionSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.post_task_conditions(data)


@router.delete(f"{CONDITION}", summary="Удаление условия задачи")
async def delete_task_conditions(
    condition_id: int,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.delete_task_conditions(condition_id)


@router.put(f"{CONDITION}", summary="Изменение условия задачи")
async def put_task_conditions(
    condition: UpdateConditionSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.put_task_conditions(condition)


@router.post(f"{DEFINE}", summary="Определение необходимых задач")
async def define_tasks(task_service: TaskService = Depends(create_task_service)):
    return await task_service.define_tasks()


@router.post(f"{DISTRIBUTION}", summary="Распределение задач по сотрудникам")
async def define_tasks(
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    begin_hour: int = Query(default=BEGIN_TIME_WORK),
    end_hour: int = Query(default=END_TIME_WORK),
    note_service: NoteService = Depends(create_note_service),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    msg, users = await task_service.distribution_tasks_to_all(begin_hour, end_hour)
    for user in users:
        send_any_message.delay(user["email"], user["msg"])
        await note_service.post_note(Note(user_id=user["id"], message=user["msg"]))
        await NoteWebsockerConnection.send_personal_message(user["msg"], user["id"])
    return msg


@router.post(
    f"{CANCELED}",
    summary=f"Задача отменена и перенесена в историю {SUPPORT_SECURITY_OWNER}",
)
async def task_cancelled(
    task: TaskCancelledSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_task_auth),
    note_service: NoteService = Depends(create_note_service),
    task_service: TaskService = Depends(create_task_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=task.id), token
    )
    msg, users = await task_service.task_cancelled(task, subject_data)
    for user in users:
        send_any_message.delay(user["email"], user["msg"])
        await note_service.post_note(Note(user_id=user["id"], message=user["msg"]))
        await NoteWebsockerConnection.send_personal_message(user["msg"], user["id"])
    return msg


@router.post(
    f"{COMPLETED}",
    summary=f"Задача выполнена и перенесена в историю {SUPPORT_SECURITY_OWNER}",
)
async def task_completed(
    data: TaskCompletedSchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_task_auth),
    note_service: NoteService = Depends(create_note_service),
    task_service: TaskService = Depends(create_task_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=data.id), token
    )
    msg, users = await task_service.task_completed(data, subject_data)
    for user in users:
        send_any_message.delay(user["email"], user["msg"])
        await note_service.post_note(Note(user_id=user["id"], message=user["msg"]))
        await NoteWebsockerConnection.send_personal_message(user["msg"], user["id"])
    return msg


@router.put(ACCEPTE, summary=f"Принять задачу {SUPPORT_SECURITY_OWNER}")
async def accept_task(
    task_id: int,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_task_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path, id=task_id), token
    )
    return await task_service.accept_task(task_id)


@router.put(CHANGE_PRIORITY, summary="Изменить приоритеты задач")
async def task_change_priority(
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.task_change_priority()


@router.put(
    "/by_manager",
    summary=f"Назначить задачу сотруднику самостоятельно {SUPPORT_SECURITY_OWNER}",
)
async def put_task_by_manager(
    id: int,
    employee_id: int,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_task_auth),
    task_service: TaskService = Depends(create_task_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await task_service.put_task_by_manager(id, employee_id)


@router.delete("/tasks", summary="Удаление всех задач")
async def delete_tasks(
    task_service: TaskService = Depends(create_task_service),
):
    return await task_service.delete_tasks()

