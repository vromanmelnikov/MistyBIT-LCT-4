from src.authorization.informants import IResourceInformantService
from src.authorization.schemas import ResourceData
from src.database.models.users.user import User
from src.services.unit_of_work import IUnitOfWork


class ProfileInformantService(IResourceInformantService):
    async def get(self, resource: ResourceData, uow: IUnitOfWork) -> ResourceData:
        user = None
        if resource.id:
            user: User = await uow.users.get_by_id(resource.id)
        return ResourceData(
            name=resource.name, id=resource.id, owner_id=user.id if user else None
        )
