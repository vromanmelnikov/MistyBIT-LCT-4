from abc import ABC, abstractmethod

from src.authentication.schemas import TokenDataSchema
from src.authorization.schemas import *
from src.services.unit_of_work import IUnitOfWork


class ISubjectInformantService(ABC):
    @abstractmethod
    async def get(self, token_data: TokenDataSchema) -> SubjectData:
        raise NotImplementedError()


class IActionInformantService(ABC):
    @abstractmethod
    async def get(self, name: str) -> ActionData:
        raise NotImplementedError()


class IResourceInformantService(ABC):
    @abstractmethod
    async def get(self, resource: ResourceData, uow: IUnitOfWork) -> ResourceData:
        raise NotImplementedError()


class AbstractUserInformantService(ISubjectInformantService):
    async def get(self, token_data: TokenDataSchema) -> SubjectData:
        # return await uow.user_abstracts.get_by_id(id)
        return SubjectData(**token_data.dict())


class ActionInformantService(IActionInformantService):
    async def get(self, name: str) -> ActionData:
        return ActionData(name=name)


class DefaultResourceInformantService(IResourceInformantService):
    async def get(self, resource: ResourceData, uow: IUnitOfWork) -> ResourceData:
        return ResourceData(name=resource.name)
