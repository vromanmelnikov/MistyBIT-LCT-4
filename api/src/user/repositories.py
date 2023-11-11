from abc import ABC, abstractmethod
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.orm import selectinload

from src.database.models import *
from src.database.repositories import GenericSqlRepository, GenericRepository
from src.database.exceptions import *
from src.database.repositories.simple import ISimpleRepository, SimpleRepository
from src.user.exceptions import *


class IRoleRepository(ISimpleRepository[Role], ABC):
    pass


class RoleRepository(SimpleRepository[Role], IRoleRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Role)


# User
class IUserRepository(GenericRepository[User], ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_login(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all_full(
        self,
        limit: int | None,
        offset: int | None,
        substr: str | None,
        role_id: int | None,
    ):
        raise NotImplementedError()


class UserRepository(GenericSqlRepository[User], IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_id(self, id: int) -> Optional[User]:
        stmt = self._construct_statement_get_by_id(id)
        stmt = stmt.options(
            selectinload(User.role),
            selectinload(User.manager),
            selectinload(User.admin),
            selectinload(User.employee).selectinload(Employee.grade),
            selectinload(User.employee).selectinload(Employee.office),
            selectinload(User.employee)
            .selectinload(Employee.skill_links)
            .selectinload(EmployeeSkillLink.skill),
        )
        return await self._execute_statement_get_by_id(stmt, id)

    async def get_by_login(self, email: str) -> Optional[User]:
        try:
            stmt = self._construct_statement_get_one(email=email)
            # stmt = stmt.options(selectinload(User.role))
            return await self._execute_statement_get_one(stmt)
        except GetOneItemException as e:
            raise GetUserByEmailException(email) from e

    async def get_all_full(
        self,
        limit: int | None,
        offset: int | None,
        substr: str | None,
        role_id: int | None,
    ):
        stmt = self._construct_statement_get_all(offset, limit)
        stmt = stmt.options(
            selectinload(User.role),
            selectinload(User.manager),
            selectinload(User.admin),
            selectinload(User.employee),
        )
        stmt = self._add_substr_to_stmt(stmt, User.lastname, substr)
        if role_id is not None:
            stmt = stmt.filter(User.role_id == role_id)
        return await self._execute_statement_get_all(stmt)


class IGradeRepository(GenericRepository[Grade], ABC):
    @abstractmethod
    async def get_all(self, limit: int | None = None, offset: int | None = None):
        raise NotImplementedError()


class GradeRepository(GenericSqlRepository[Grade], IGradeRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Grade)

    async def get_all(self, limit: int | None = None, offset: int | None = None):
        stmt = self._construct_statement_get_all(offset, limit).order_by(
            Grade.value.desc()
        )
        return await self._execute_statement_get_all(stmt)


class ISkillRepository(GenericRepository[Skill], ABC):
    pass


class SkillRepository(GenericSqlRepository[Skill], ISkillRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Skill)


class IEmployeeSkillRepository(GenericRepository[EmployeeSkillLink], ABC):
    pass


class EmployeeSkillRepository(
    GenericSqlRepository[EmployeeSkillLink], IEmployeeSkillRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, EmployeeSkillLink)


class IEmployeeRepository(GenericRepository[Employee], ABC):
    @abstractmethod
    async def get_all_full(
        limit: int | None = None,
        offset: int | None = None,
        substr: str | None = None,
        office_id: int | None = None,
        is_active: bool = True,
    ):
        raise NotImplementedError()


class EmployeeRepository(GenericSqlRepository[Employee], IEmployeeRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Employee)

    async def get_all_full(
        self,
        limit: int | None = None,
        offset: int | None = None,
        substr: str | None = None,
        office_id: int | None = None,
        is_active: bool = True,
    ):
        stmt = self._construct_statement_get_all(offset, limit)
        stmt = stmt.options(
            selectinload(Employee.user),
            selectinload(Employee.grade),
            selectinload(Employee.office),
            selectinload(Employee.skill_links).selectinload(EmployeeSkillLink.skill),
        )
        if is_active:
            stmt = stmt.join(User).where(User.is_active)
        if substr is not None:
            sub = self._constructor_subquery(User, [], lastname=substr)
            stmt = stmt.join(sub)
        if office_id is not None:
            stmt = stmt.filter(Employee.office_id == office_id)
        return await self._execute_statement_get_all(stmt)


class IManagerRepository(GenericRepository[Manager], ABC):
    @abstractmethod
    async def get_all():
        raise NotImplementedError()


class ManagerRepository(GenericSqlRepository[Manager], IManagerRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Manager)

    async def get_all(self):
        stmt = self._construct_statement_get_all()
        stmt = stmt.options(selectinload(Manager.user))
        return await self._execute_statement_get_all(stmt)
