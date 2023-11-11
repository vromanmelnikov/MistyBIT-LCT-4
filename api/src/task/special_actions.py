from abc import ABC, abstractmethod

from src.services.unit_of_work import IUnitOfWork
from src.task.const import DELIVERY_CARD_TYPE_ID


class SpecialActionBase(ABC):
    def __init__(self, type_task_id: int):
        self.type_task_id = type_task_id

    def _check_match_id(self, inp_id: int):
        return self.type_task_id == inp_id

    @abstractmethod
    async def execute(self, type_task_id: int, uow: IUnitOfWork, **kwargs) -> bool:
        raise NotImplementedError()


class DeliveryCardSpecialAction(SpecialActionBase):
    def __init__(self):
        super().__init__(DELIVERY_CARD_TYPE_ID)

    async def execute(self, type_task_id: int, uow: IUnitOfWork, **kwargs):
        if self._check_match_id(type_task_id):
            point_id = kwargs.get("point_id", None)
            if point_id:
                point = await uow.points.get_by_id(point_id)
                point.is_delivered_card = True
                await uow.commit()
                return True
        return False
