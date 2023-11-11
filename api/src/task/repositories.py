from abc import ABC, abstractmethod
from redis import Redis
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import *
from src.database.exceptions import *
from src.database.repositories.generic_redis import GenericRedisRepository
from src.database.repositories.simple import ISimpleRepository, SimpleRepository
from src.task.schemas import BlockTaskSchema
from src.user.exceptions import *
from src.database.repositories.generic import GenericRepository
from src.database.repositories.generic_sqlalchemy import GenericSqlRepository
from src.database.schemas import RecordRedisSchema
from datetime import datetime


class ITypeTaskRepository(ISimpleRepository[TypeTask], ABC):
    pass


class TypeTaskRepository(SimpleRepository[TypeTask], ITypeTaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TypeTask)


class IPriorityRepository(GenericRepository[Priority], ABC):
    pass


class PriorityRepository(GenericSqlRepository[Priority], IPriorityRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Priority)


class ITaskStatusRepository(GenericRepository[TaskStatus], ABC):
    pass


class TaskStatusRepository(GenericSqlRepository[TaskStatus], ITaskStatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TaskStatus)


class IConditionRepository(GenericRepository[Condition], ABC):
    pass


class ConditionRepository(GenericSqlRepository[Condition], IConditionRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Condition)


class IBlockTaskRepository(GenericRepository[RecordRedisSchema], ABC):
    @abstractmethod
    async def get_by_id(task_id: int, point_id: int):
        raise NotImplementedError()


class BlockTaskRepository(
    GenericRedisRepository[BlockTaskSchema], IBlockTaskRepository
):
    def __init__(self, redis_connect: Redis) -> None:
        super().__init__(redis_connect, BlockTaskSchema)

    def __gen_key(self, task_id: int, point_id: int):
        return f"{task_id}_{point_id}"

    async def get_by_id(self, task_id: int, point_id: int):
        key = self.__gen_key(task_id, point_id)
        return await super().get_by_id(key)

    async def add(self, record: BlockTaskSchema) -> bool:
        try:
            key = self.__gen_key(record.task_id, record.point_id)
            return await self._redis_connect.set(key, bool, record.interval)
        except Exception as e:
            raise AddItemException()


class ITaskRepository(GenericRepository[Task], ABC):
    @abstractmethod
    async def get_all_full(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def get_all_full_front(
        self,
        limit: int | None,
        offset: int | None,
        type_id: int | None,
        point_id: int | None,
        status_id: int | None,
        priority_id: int | None,
        employee_id: int | None,
        date_create: datetime | None,
        date_begin: datetime | None,
        to_all: bool = True,
    ):
        raise NotImplementedError()

    @abstractmethod
    async def delete_all(self):
        raise NotImplementedError()


class TaskRepository(GenericSqlRepository[Task], ITaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Task)

    async def get_all_full(self, **kwargs):
        stmt = self._construct_statement_get_all(**kwargs)
        stmt = (
            stmt.join(Priority)
            .options(
                selectinload(Task.type)
                .selectinload(TypeTask.skill_links)
                .selectinload(TypeTaskSkillLinks.skill),
                selectinload(Task.type)
                .selectinload(TypeTask.grade_links)
                .selectinload(TypeTaskGradeLink.grade),
                selectinload(Task.priority),
                selectinload(Task.point),
            )
            .order_by(Priority.value.desc(), Task.date_create)
        )
        return await self._execute_statement_get_all(stmt)

    async def get_all_full_front(
        self,
        limit: int | None,
        offset: int | None,
        type_id: int | None,
        point_id: int | None,
        status_id: int | None,
        priority_id: int | None,
        employee_id: int | None,
        date_create: datetime | None,
        date_begin: datetime | None,
        to_all: bool = True,
    ):
        stmt = self._construct_statement_get_all(offset, limit)
        stmt = stmt.options(
            selectinload(Task.point),
            selectinload(Task.priority),
            selectinload(Task.status),
            selectinload(Task.employee).selectinload(Employee.user),
            selectinload(Task.employee).selectinload(Employee.grade),
            selectinload(Task.employee).selectinload(Employee.office),
            selectinload(Task.type)
            .selectinload(TypeTask.skill_links)
            .selectinload(TypeTaskSkillLinks.skill),
            selectinload(Task.type)
            .selectinload(TypeTask.grade_links)
            .selectinload(TypeTaskGradeLink.grade),
        )
        if to_all:
            stmt = stmt.order_by(Task.date_create)
        else:
            stmt = stmt.order_by(Task.status_id.desc(), Task.date_begin)
        if type_id is not None:
            stmt = stmt.filter(Task.type_id == type_id)
        if point_id is not None:
            stmt = stmt.filter(Task.point_id == point_id)
        if status_id is not None:
            stmt = stmt.filter(Task.status_id == status_id)
        if priority_id is not None:
            stmt = stmt.filter(Task.priority_id == priority_id)
        if employee_id is not None:
            stmt = stmt.filter(Task.employee_id == employee_id)
        if date_create is not None:
            stmt = stmt.filter(Task.date_create >= date_create)
        if date_begin is not None:
            stmt = stmt.filter(Task.date_begin >= date_begin)
        return await self._execute_statement_get_all(stmt)

    async def delete_all(self):
        await self._session.execute(delete(Task))


class ITypeTaskRepository(GenericRepository[TypeTask], ABC):
    @abstractmethod
    async def get_all_full(self):
        raise NotImplementedError()


class TypeTaskRepository(GenericSqlRepository[TypeTask], ITypeTaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TypeTask)

    async def get_all_full(self):
        stmt = self._construct_statement_get_all(None, None)
        stmt = (
            stmt.join(Priority)
            .options(
                selectinload(TypeTask.grade_links).selectinload(
                    TypeTaskGradeLink.grade
                ),
                selectinload(TypeTask.skill_links).selectinload(
                    TypeTaskSkillLinks.skill
                ),
                selectinload(TypeTask.conditions),
                selectinload(TypeTask.priority),
            )
            .order_by(Priority.value)
        )
        return await self._execute_statement_get_all(stmt)


class ITypeTaskGradeRepository(GenericRepository[TypeTaskGradeLink], ABC):
    pass


class TypeTaskGradeRepository(
    GenericSqlRepository[TypeTaskGradeLink], ITypeTaskGradeRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TypeTaskGradeLink)


class ITypeTaskSkillRepository(GenericRepository[TypeTaskSkillLinks], ABC):
    pass


class TypeTaskSkillRepository(
    GenericSqlRepository[TypeTaskSkillLinks], ITypeTaskSkillRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TypeTaskSkillLinks)


class IHistoryTaskRepository(GenericRepository[HistoryTask], ABC):
    @abstractmethod
    async def get_all(
        self, limit: int | None, offset: int | None, employee_id: int | None
    ):
        raise NotImplementedError()


class HistoryTaskRepository(GenericSqlRepository[HistoryTask], IHistoryTaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, HistoryTask)

    async def get_all(
        self, limit: int | None, offset: int | None, employee_id: int | None
    ):
        stmt = self._construct_statement_get_all(offset, limit)
        if employee_id is not None:
            stmt = stmt.filter(HistoryTask.employee_id == employee_id)
        stmt = stmt.order_by(
            HistoryTask.date_begin.desc(), HistoryTask.date_create.desc()
        )
        return await self._execute_statement_get_all(stmt)


class INoteRepository(GenericRepository[Note], ABC):
    pass


class NoteRepository(GenericSqlRepository[Note], INoteRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Note)
