from abc import ABC, abstractmethod
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from src.authorization.repositories import *
from src.user.repositories import *
from src.task.repositories import *
from src.office.repositories import *
from src.authentication.repositories import *


class IUnitOfWork(ABC):
    # auth
    pswd_recoveries: IPasswordRecoveryRepository

    # USER
    users: IUserRepository
    roles: IRoleRepository
    grades: IGradeRepository
    skills: ISkillRepository
    employee_skills: IEmployeeSkillRepository
    managers: IManagerRepository
    employees: IEmployeeRepository

    # TASK
    priorities: IPriorityRepository
    task_statuses: ITaskStatusRepository
    type_tasks: ITypeTaskRepository
    type_task_skills: ITypeTaskSkillRepository
    type_task_grades: ITypeTaskGradeRepository
    task_conditions: IConditionRepository
    tasks: ITaskRepository
    block_tasks: IBlockTaskRepository
    history_tasks: IHistoryTaskRepository
    notes: INoteRepository

    # OFFICE
    offices: IOfficeRepository
    points: IPointRepository
    point_durations: IPointDurationRepository
    office_durations: IOfficeDurationRepository
    traffics: ITrafficRepository

    policies: IPolicyRepository

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self):
        pass

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(IUnitOfWork):
    def __init__(self, session_maker: Callable[[], AsyncSession], redis_conect: Redis):
        self.__session_maker = session_maker
        self.__redis_conect = redis_conect

    async def __aenter__(self):
        self.__session: AsyncSession = self.__session_maker()
        # auth
        self.pswd_recoveries = PasswordRecoveryRepository(self.__redis_conect)

        # USER
        self.users = UserRepository(self.__session)
        self.roles = RoleRepository(self.__session)
        self.grades = GradeRepository(self.__session)
        self.skills = SkillRepository(self.__session)
        self.employee_skills = EmployeeSkillRepository(self.__session)
        self.managers = ManagerRepository(self.__session)
        self.employees = EmployeeRepository(self.__session)

        # TASK
        self.priorities = PriorityRepository(self.__session)
        self.task_statuses = TaskStatusRepository(self.__session)
        self.type_tasks = TypeTaskRepository(self.__session)
        self.type_task_grades = TypeTaskGradeRepository(self.__session)
        self.type_task_skills = TypeTaskSkillRepository(self.__session)
        self.task_conditions = ConditionRepository(self.__session)
        self.tasks = TaskRepository(self.__session)
        self.block_tasks = BlockTaskRepository(self.__redis_conect)
        self.history_tasks = HistoryTaskRepository(self.__session)
        self.notes = NoteRepository(self.__session)

        # OFFICE
        self.offices = OfficeRepository(self.__session)
        self.points = PointRepository(self.__session)
        self.point_durations = PointDurationRepository(self.__session)
        self.office_durations = OfficeDurationRepository(self.__session)
        self.traffics = TrafficRepository(self.__session)

        self.policies = PolicyRepository(self.__session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await self.rollback()
        await self.__session.close()

    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()
