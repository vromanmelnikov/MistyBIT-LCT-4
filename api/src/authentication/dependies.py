from fastapi import Depends

from src.authentication.service import AuthenticationService
from src.dependies import create_uow
from src.services import IUnitOfWork


def create_authentication_service(
    uow: IUnitOfWork = Depends(create_uow),
):
    return AuthenticationService(uow)
