import vakt
from vakt.rules import Eq, Truthy

from src.const import *
from src.utils import IncrementorId
from src.office.const import COMMON_URL as OFFICE_COMMON_URL, POINTS
from src.user.const import (
    COMMON_URL as USER_COMMON_URL,
    EMPLOYEE,
    EMPLOYEES,
    IS_ACTIVE,
    PROFILE,
    REGISTRATION,
    SKILLS,
)
from src.task.const import *
from src.authorization.const import *


Incrementor = IncrementorId()

policies = [
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_GET)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{PROFILE}")}],
        subjects=[
            {"role_id": Eq(ROLE_ADMIN)},
            {"role_id": Eq(ROLE_MANAGER)},
            {"role_id": Eq(ROLE_EMPLOYEE), "is_owner": Truthy()},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Администраторы и менеджры могут просматривать все профили, пользователь только свой",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{REGISTRATION}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только администраторы могут добавлять новых пользователей",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}/")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут удалять офисы",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}/")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут изменять офисы",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{SKILLS}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджеры могут добавлять навыки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{SKILLS}{EMPLOYEE}")}],
        subjects=[{"role_id": Eq(ROLE_EMPLOYEE)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только сотрудники могут добавлять навыки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{SKILLS}{EMPLOYEE}")}],
        subjects=[{"role_id": Eq(ROLE_EMPLOYEE)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только сотрудники могут удалять свои навыки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}/")}],
        subjects=[
            {"role_id": Eq(ROLE_ADMIN)},
            {"role_id": Eq(ROLE_MANAGER)},
            {"role_id": Eq(ROLE_EMPLOYEE), "is_owner": Truthy()},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Администраторы и менеджеры могут изменять любой профиль, сотрудники только свой",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}/")}],
        subjects=[
            {"role_id": Eq(ROLE_ADMIN)},
            {"role_id": Eq(ROLE_MANAGER)},
            {"role_id": Eq(ROLE_EMPLOYEE), "is_owner": Truthy()},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Все могут удалять свой профиль",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}{IMMAGE}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может изменять картинку офиса",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}{POINTS}{IMMAGE}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может изменять картинку точки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{IMMAGE}")}],
        subjects=[
            {"role_id": Eq(ROLE_ADMIN)},
            {"role_id": Eq(ROLE_EMPLOYEE)},
            {"role_id": Eq(ROLE_MANAGER)},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Все могут изменять картинку своего профиля",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{IMMAGE}")}],
        subjects=[
            {"role_id": Eq(ROLE_ADMIN)},
            {"role_id": Eq(ROLE_EMPLOYEE)},
            {"role_id": Eq(ROLE_MANAGER)},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Все могут удалять картинку профиля",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}/")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут добавлять офисы",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{IS_ACTIVE}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут переводить сотрудника в актив/неактив",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{EMPLOYEES}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджеры могут изменять грейд и офис сотрудника",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}{POINTS}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут добавлять точки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}{POINTS}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут изменять точки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{OFFICE_COMMON_URL}{POINTS}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут удалять точки",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может добавлять типы задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может изменять типы задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может удалять типы задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}{GRADES}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может добавлять грейды для типов задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}{GRADES}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может удалять грейды для типов задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}{SKILLS}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может добавлять навыки для типов задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{TYPES}{SKILLS}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может удалять навыки для типов задач",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{CONDITION}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может добавлять условия к типу задачи",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_DELETE)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{CONDITION}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может удалять условия у типа задачи",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{CONDITION}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может изменять условия у типа задачи",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_GET)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{ALL}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут просматривать всех пользователей",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_GET)}],
        resources=[{"name": Eq(f"{USER_COMMON_URL}{EMPLOYEES}{ALL}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}, {"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы и менеджеры могут просматривать всех сотрудников",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_GET)}],
        resources=[{"name": Eq(f"{SECURITY_COMMON_URL}{METHODS}{ALL}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут просматривать защищенные методы",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_GET)}],
        resources=[{"name": Eq(f"{SECURITY_COMMON_URL}{POLICIES}{ALL}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут просматривать политики безопасности защищенных методов",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{SECURITY_COMMON_URL}{POLICIES}")}],
        subjects=[{"role_id": Eq(ROLE_ADMIN)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только админы могут изменять политики безопасности защищенных методов",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{COMPLETED}")}],
        subjects=[
            {"role_id": Eq(ROLE_MANAGER)},
            {"role_id": Eq(ROLE_EMPLOYEE), "is_owner": Truthy()},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Менеджеры могут завершать задачи а сотрудники только свои задачи",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{CANCELED}")}],
        subjects=[
            {"role_id": Eq(ROLE_MANAGER)},
            {"role_id": Eq(ROLE_EMPLOYEE), "is_owner": Truthy()},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Менеджеры могут отменять задачи а сотрудники только свои задачи",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_POST)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{DISTRIBUTION}")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджеры могут распределять задачи по сотрудникам",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}{ACCEPTE}")}],
        subjects=[{"role_id": Eq(ROLE_EMPLOYEE), "is_owner": Truthy()}],
        effect=vakt.ALLOW_ACCESS,
        description="Только сотрудники могут принять свои задачи",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_PUT)}],
        resources=[{"name": Eq(f"{TASK_COMMON_URL}/by_manager")}],
        subjects=[{"role_id": Eq(ROLE_MANAGER)}],
        effect=vakt.ALLOW_ACCESS,
        description="Только менеджер может назначать задачи сотруднику",
    ),
    vakt.Policy(
        Incrementor.get_value(),
        actions=[{"name": Eq(REST_API_GET)}],
        resources=[{"name": Eq(f"/notifications/")}],
        subjects=[
            {"role_id": Eq(ROLE_ADMIN)},
            {"role_id": Eq(ROLE_MANAGER)},
            {"role_id": Eq(ROLE_EMPLOYEE)},
        ],
        effect=vakt.ALLOW_ACCESS,
        description="Все могут получать свои уведомления",
    ),
]
