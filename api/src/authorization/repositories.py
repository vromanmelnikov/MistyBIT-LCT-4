from abc import ABC, abstractmethod
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.orm import selectinload

from src.database.models import *
from src.database.repositories import GenericSqlRepository, GenericRepository
from src.database.exceptions import *
from src.user.exceptions import *


class IPolicyRepository(GenericRepository[VaktPolicy], ABC):
    pass


class PolicyRepository(GenericSqlRepository[VaktPolicy], IPolicyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, VaktPolicy)
