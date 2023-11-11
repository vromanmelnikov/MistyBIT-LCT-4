from abc import ABC
from typing import List, Optional, Type, TypeVar
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from sqlalchemy.sql import Select
from sqlalchemy.sql.selectable import Subquery
from sqlalchemy.exc import IntegrityError

from src.database.exceptions import *
from src.database.repositories.generic import GenericRepository

T = TypeVar("T")


class GenericSqlRepository(GenericRepository[T], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    async def get_all(
        self, offset: int | None = None, limit: int | None = None, **filters
    ) -> List[T]:
        stmt = self._construct_statement_get_all(offset, limit, **filters)
        return await self._execute_statement_get_all(stmt)

    async def get_one(self, **filters) -> Optional[T]:
        stmt = self._construct_statement_get_one(**filters)
        return await self._execute_statement_get_one(stmt)

    async def get_by_id(self, id: int) -> Optional[T]:
        stmt = self._construct_statement_get_by_id(id)
        return await self._execute_statement_get_by_id(stmt, id)

    async def add(self, record: T) -> T:
        try:
            self._session.add(record)
            await self._session.flush()
            await self._session.refresh(record)
            return record
        except IntegrityError as e:
            if e.orig.__cause__.__class__ == UniqueViolationError:
                raise UniqueViolationException(e.args[0])
            if e.orig.__cause__.__class__ == ForeignKeyViolationError:
                raise ForeignKeyViolationException(self._model_cls.__name__)
            raise AddItemException(self._model_cls.__name__)
        except Exception as e:
            raise AddItemException(self._model_cls.__name__)

    async def add_all(self, records: list[T]) -> bool:
        try:
            self._session.add_all(records)
            return True
        except IntegrityError as e:
            if e.orig.__cause__.__class__ == UniqueViolationError:
                raise UniqueViolationException(e.args[0])
            if e.orig.__cause__.__class__ == ForeignKeyViolationError:
                raise ForeignKeyViolationException(self._model_cls.__name__)
            raise AddItemException(self._model_cls.__name__)
        except Exception as e:
            raise AddItemException(self._model_cls.__name__)

    async def delete(self, **filters) -> None:
        try:
            record = await self.get_one(**filters)
            if record is not None:
                await self._session.delete(record)
                await self._session.flush()
        except Exception as e:
            raise DeleteItemException(self._model_cls.__name__) from None

    def _add_substr_to_stmt(self, stmt: Select, column, substr: str | None) -> Select:
        """Добавление поиска по подстроке

        Args:
            stmt (Select): statement
            column (str): Название столбца
            substr (str): Подстрока

        Returns:
            Select: Собранный statement
        """
        if substr:
            return stmt.where(column.ilike(f"%{substr}%"))
        return stmt

    def _construct_statement_get_all(
        self, offset: int | None=None, limit: int | None=None, **filters
    ) -> Select:
        """Конструктор statement для метода получения всех элементов

        Args:
            offset (int | None): Смешение
            limit (int | None): Ограничение количества элементов

        Returns:
            Select: Собранный statement
        """
        stmt = self._construct_list_stmt(**filters)
        stmt = self._add_limit_offset_to_stmt(stmt, limit, offset)
        return stmt

    def _add_limit_offset_to_stmt(
        self, stmt: Select, limit: int | None, offset: int | None
    ):
        if offset and limit:
            stmt = stmt.limit(limit).offset(offset * limit)
        elif limit:
            stmt = stmt.limit(limit)
        return stmt

    def _construct_statement_get_one(self, **filters) -> Select:
        """Конструктор statement для метода получения одного элемента

        Returns:
            Select: Собранный statement
        """
        return self._construct_list_stmt(**filters)

    def _construct_statement_get_by_id(self, id: int) -> Select:
        """Конструктор statement для метода получения одного элемента по id

        Args:
            id (int): id элемента

        Returns:
            Select: Собранный statement
        """
        return self._construct_get_stmt(id)

    def _construct_get_stmt(self, id: int) -> Select:
        """Конструктор statement для получения элемента по id

        Args:
            id (int): id элемента

        Returns:
            Select: Собранный statement
        """
        return select(self._model_cls).where(self._model_cls.id == id)

    def _construct_list_stmt(self, is_internal=True, table=None, **filters) -> Select:
        """Конструктор statement для получения на основе фильтров

        Raises:
            InvalidColumnException: Неизвестный столбец для фильтрации

        Returns:
            Select: Собранный statement
        """
        model = self._model_cls if is_internal else table
        stmt = select(model)
        where_clauses = []
        for column, value in filters.items():
            if value is None:
                continue
            if not hasattr(model, column):
                raise InvalidColumnException(column) from None
            where_clauses.append(getattr(model, column) == value)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    def _constructor_subquery(
        self, table, join_tables: list = [], **filters
    ) -> Subquery:
        tmp = self._construct_list_stmt(is_internal=False, table=table, **filters)
        for t in join_tables:
            tmp.join(t)
        return tmp.subquery()

    async def _execute_statement_get_all(self, statement: Select) -> List[T]:
        """Выполнения statement для метода получения всех элементов

        Args:
            statement (Select): Собранный statement

        Raises:
            GetAllItemsException: Ошибка получения всех элементов

        Returns:
            List[T]: Список полученных элементов
        """
        try:
            result = await self._session.execute(statement)
            return result.scalars().all()
        except Exception as e:
            raise GetAllItemsException(self._model_cls.__name__) from None

    async def _execute_statement_get_one(self, statement: Select) -> Optional[T]:
        """Выполнения statement для метода получения одного элемента

        Args:
            statement (Select): Собранный statement

        Raises:
            GetOneItemException: Ошибка получения элемента

        Returns:
            Optional[T]: Один элемент, который может быть None
        """
        try:
            result = await self._session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as e:
            raise GetOneItemException(self._model_cls.__name__) from None

    async def _execute_statement_get_by_id(self, statement: Select, id: int):
        """Выполнения statement для метода получения одного элемента

        Args:
            statement (Select): Собранный statement
            id (int): id элемента

        Raises:
            GetItemByIdException: Ошибка получения элемента по id

        Returns:
            Optional[T]: Один элемент, который может быть None
        """
        try:
            result = await self._session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as e:
            raise GetItemByIdException(self._model_cls.__name__, id) from None
