from src.database.base import AsyncSessionMaker
from src.services.unit_of_work import UnitOfWork
from src.config import RedisConnection


def create_uow():
    return UnitOfWork(AsyncSessionMaker, RedisConnection)
