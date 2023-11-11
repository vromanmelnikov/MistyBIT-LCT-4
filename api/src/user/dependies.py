from fastapi import Depends
from src.authorization.dependies import FactoryAuthorizationService
from src.const import *

from src.dependies import *
from src.services import *
from src.user.informants import ProfileInformantService
from src.user.mappers import EmployeeMapper, ManagerMapper
from src.user.schemas import TypeSelectMapperSchema
from src.user.service import UserService


def create_user_service(
    uow: IUnitOfWork = Depends(create_uow),
):
    employee = TypeSelectMapperSchema(EmployeeMapper(), REPOSITORY_EMPLOYEE)
    manager = TypeSelectMapperSchema(ManagerMapper(), REPOSITORY_MANAGER)
    return UserService(uow, {ROLE_EMPLOYEE: employee, ROLE_MANAGER: manager})


def create_user_informant_service():
    return ProfileInformantService()


factory_user_auth = FactoryAuthorizationService(
    resource_InformantService=create_user_informant_service()
)
