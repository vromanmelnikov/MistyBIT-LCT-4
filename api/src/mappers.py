from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

from src.database.schemas import RecordRedisSchema

T = TypeVar("T")


class BaseMapper(Generic[T], ABC):
    @abstractmethod
    def create_from_database(self, item) -> T:
        raise NotImplementedError()

    @abstractmethod
    def create_from_input(self, item):
        raise NotImplementedError()


class SimpleMapper(BaseMapper[T], ABC):
    def __init__(self, schema: Type[T]):
        self._schema = schema

    def create_from_database(self, item) -> T:
        return self._schema.from_orm(item)

    def create_from_input(self, item):
        raise NotImplementedError()


class RecordRedisMapper(BaseMapper[RecordRedisSchema]):
    def create_from_input(self, key: str, value: Any, expire: int = 0):
        return RecordRedisSchema(key=key, value=value, expire=expire)

    def create_from_database(sellf, item):
        return item.value
