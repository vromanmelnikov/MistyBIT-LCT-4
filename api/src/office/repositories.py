from abc import ABC, abstractmethod
from sqlalchemy import delete, or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.orm import selectinload

from src.database.models import *
from src.database.repositories import GenericSqlRepository, GenericRepository
from src.database.exceptions import *
from src.user.exceptions import *


class IOfficeRepository(GenericRepository[Office], ABC):
    @abstractmethod
    async def get_all_full(
        self, limit: int | None, offset: int | None, substr: str | None
    ):
        raise NotImplementedError()


class OfficeRepository(GenericSqlRepository[Office], IOfficeRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Office)

    async def get_all_full(
        self, limit: int | None, offset: int | None, substr: str | None
    ):
        stmt = self._construct_statement_get_all(offset, limit)
        stmt = stmt.options()
        stmt = self._add_substr_to_stmt(stmt, Office.address, substr)
        return await self._execute_statement_get_all(stmt)


class IPointRepository(GenericRepository[Point], ABC):
    @abstractmethod
    async def execute_stmt_all(self, stmt):
        raise NotImplementedError()
        return self._execute_statement_get_all()

    @abstractmethod
    async def get_all_full(
        self, limit: int | None, offset: int | None, substr: str | None
    ):
        raise NotImplementedError()


class PointRepository(GenericSqlRepository[Point], IPointRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Point)

    async def get_all_full(
        self, limit: int | None, offset: int | None, substr: str | None
    ):
        stmt = self._construct_statement_get_all(offset, limit)
        stmt = stmt.options()
        stmt = self._add_substr_to_stmt(stmt, Point.address, substr)
        return await self._execute_statement_get_all(stmt)

    async def execute_stmt_all(self, stmt):
        return await self._execute_statement_get_all(stmt)


class IPointDurationRepository(GenericRepository[PointDuration], ABC):
    @abstractmethod
    async def delete_all(self):
        raise NotImplementedError()


class PointDurationRepository(
    GenericSqlRepository[PointDuration], IPointDurationRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PointDuration)

    async def delete_all(self):
        await self._session.execute(delete(PointDuration))


class IOfficeDurationRepository(GenericRepository[OfficeDuration], ABC):
    @abstractmethod
    async def delete_all(self):
        raise NotImplementedError()


class OfficeDurationRepository(
    GenericSqlRepository[OfficeDuration], IOfficeDurationRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OfficeDuration)

    async def delete_all(self):
        await self._session.execute(delete(OfficeDuration))


class ITrafficRepository(GenericRepository[Traffic], ABC):
    @abstractmethod
    async def delete_all(self):
        raise NotImplementedError()


class TrafficRepository(GenericSqlRepository[Traffic], ITrafficRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Traffic)

    async def delete_all(self):
        await self._session.execute(delete(Traffic))
