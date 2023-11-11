from fastapi import Depends
from src.authorization.dependies import FactoryAuthorizationService

from src.dependies import *
from src.services import *
from src.task.informants import TaskInformantService
from src.task.operators import *
from src.task.service import TaskService
from src.task.special_actions import DeliveryCardSpecialAction


def create_task_service(
    uow: IUnitOfWork = Depends(create_uow),
):
    special_actions = [DeliveryCardSpecialAction()]

    operators = [
        AdditionOperator(),
        SubtractionOperator(),
        MultiplyOperator(),
        DivisionOperator(),
        MoreOperator(),
        MoreEqualOperator(),
        LessOperator(),
        LessEqualOperator(),
        EqualOperator(),
        NotEqualOperator(),
        LessDayAgainOperator(),
        MoreDayAfterOperator(),
        EqualDayAgainOperator(),
        EqualDayAfterOperator(),
    ]
    return TaskService(uow, operators, special_actions)


def create_task_informant_service():
    return TaskInformantService()


factory_task_auth = FactoryAuthorizationService(
    resource_InformantService=create_task_informant_service()
)
