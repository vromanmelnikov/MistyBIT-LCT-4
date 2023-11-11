from abc import ABC, abstractmethod
from redis import Redis

from src.authentication.schemas import ResetPasswordSchema
from src.database.models import *
from src.database.repositories import GenericRedisRepository, GenericRepository
from src.database.schemas import RecordRedisSchema


class IPasswordRecoveryRepository(GenericRepository[RecordRedisSchema], ABC):
    @abstractmethod
    async def pop(key: str):
        raise NotImplementedError()


class PasswordRecoveryRepository(
    GenericRedisRepository[ResetPasswordSchema], IPasswordRecoveryRepository
):
    def __init__(self, redis_connect: Redis) -> None:
        super().__init__(redis_connect, ResetPasswordSchema)

    async def pop(self, key: str):
        record = await self.get_by_id(key)
        await self.delete(key)
        return record
