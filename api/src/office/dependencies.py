from fastapi import Depends

from src.dependies import *
from src.office.service import OfficeService
from src.services import *


def create_office_service(
    uow: IUnitOfWork = Depends(create_uow),
):
    return OfficeService(uow)
