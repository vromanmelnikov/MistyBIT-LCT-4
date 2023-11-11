from fastapi import status
from src.authentication.phrases import *

from src.exceptions import ServiceException


class AuthException(ServiceException):
    def __init__(self, message: str, code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message=message, code=code)


class InviteNoExistException(ServiceException):
    def __init__(
        self,
        message: str = INVITE_NOT_FOUND,
        code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message=message, code=code)


class InvalidUsernameException(ServiceException):
    def __init__(
        self, message: str = INVALID_USERNAME, code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(message=message, code=code)
