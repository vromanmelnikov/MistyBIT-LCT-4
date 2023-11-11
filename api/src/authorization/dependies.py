from fastapi import Depends
from src.authentication.dependies import create_authentication_service

from src.authorization.authorization import AuthorizationService
from src.authorization.informants import *
from src.services.unit_of_work import IUnitOfWork
from src.dependies import create_uow


def create_default_action_resource_InformantService():
    return ActionInformantService()


def create_default_subject_resource_InformantService():
    return AbstractUserInformantService()


class FactoryAuthorizationService:
    def __init__(
        self,
        resource_InformantService: IResourceInformantService = DefaultResourceInformantService(),
        action_InformantService: IActionInformantService | None = None,
        subject_InformantService: ISubjectInformantService | None = None,
    ):
        """Конструктор фабрики сервисов авторизации

        Args:
            resource_InformantService (IResourceInformantService, optional): Чаще всего надо создавать класс
            и передавать экзмпляр информатора. Defaults to DefaultResourceInformantService().
        """
        self.resource_InformantService = resource_InformantService
        self.action_InformantService = action_InformantService
        self.subject_InformantService = subject_InformantService

    def __call__(
        self,
        uow: IUnitOfWork = Depends(create_uow),
        action_InformantService: IActionInformantService = Depends(
            create_default_action_resource_InformantService
        ),
        subject_InformantService: ISubjectInformantService = Depends(
            create_default_subject_resource_InformantService
        ),
        authenticate_service: AuthorizationService = Depends(
            create_authentication_service
        ),
    ):
        return AuthorizationService(
            uow,
            authenticate_service,
            self.resource_InformantService,
            action_InformantService or self.action_InformantService,
            subject_InformantService or self.subject_InformantService,
        )


factory_default_auth = FactoryAuthorizationService()
