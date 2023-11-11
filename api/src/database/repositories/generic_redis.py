from abc import ABC
from typing import Generic, Optional, Type, TypeVar
from redis import Redis

from src.database.exceptions import AddItemException
from src.database.repositories.generic import GenericRepository
from src.database.schemas import RecordRedisSchema

T = TypeVar("T")


class GenericRedisRepository(GenericRepository[RecordRedisSchema], Generic[T], ABC):
    def __init__(self, redis_connect: Redis, model_cls: Type[T]) -> None:
        self._redis_connect = redis_connect
        self._model_cls = model_cls

    async def get_all(self, offset: int, limit: int, **filters):
        raise NotImplementedError()

    async def get_one(self, **filters):
        raise NotImplementedError()

    async def get_by_id(self, key: str) -> Optional[T]:
        return await self._redis_connect.get(key)

    async def add(self, record: RecordRedisSchema) -> bool:
        try:
            return await self._redis_connect.set(
                record.key, record.value, record.expire
            )
        except Exception as e:
            raise AddItemException()

    async def add_all(self, records: list[RecordRedisSchema]) -> bool:
        raise NotImplementedError()

    async def update(self, record: RecordRedisSchema):
        raise NotImplementedError()

    async def delete(self, key: str) -> None:
        return await self._redis_connect.delete(key)
