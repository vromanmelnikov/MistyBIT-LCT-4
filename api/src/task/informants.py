from src.authorization.informants import IResourceInformantService
from src.authorization.schemas import ResourceData
from src.database.models.users.user import User
from src.services.unit_of_work import IUnitOfWork


class TaskInformantService(IResourceInformantService):
    async def get(self, resource: ResourceData, uow: IUnitOfWork) -> ResourceData:
        task = None
        if resource.id:
            task: User = await uow.tasks.get_by_id(resource.id)
        return ResourceData(
            name=resource.name,
            id=resource.id,
            owner_id=task.employee_id if task else None,
        )
