from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar, Type

from src.database.models import *
from src.database.repositories import GenericSqlRepository, GenericRepository

T = TypeVar("T")


class ISimpleRepository(GenericRepository[T], ABC):
    @abstractmethod
    async def get_all(
        self, offset: int | None, limit: int | None, substr: str | None, **filters
    ) -> List[T]:
        raise NotImplementedError()


class SimpleRepository(GenericSqlRepository[T], ISimpleRepository):
    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        super().__init__(session, model_cls)

    async def _core_get_all(
        self, offset: int | None, limit: int | None, substr: str | None, **filters
    ) -> List[T]:
        stmt = self._construct_statement_get_all(offset, limit, **filters)
        stmt = self._add_substr_to_stmt(stmt, self._model_cls.name, substr).order_by(
            self._model_cls.name
        )
        return await self._execute_statement_get_all(stmt)

    async def get_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        substr: str | None = None,
        **filters
    ) -> List[T]:
        return await self._core_get_all(offset, limit, substr, **filters)
