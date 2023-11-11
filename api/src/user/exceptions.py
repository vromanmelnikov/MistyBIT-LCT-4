from fastapi import status

from src.database.exceptions import DBException
from src.exceptions import ServiceException
from src.user.phrases import (
    GET_USER_BY_ID_EXCEPTION,
    RESET_EMAIL_FAILED,
)


class GetUserByEmailException(DBException):
    """Ошибка получения пользователя по email"""

    def __init__(self, email: str):
        super().__init__(f"Не удалось получить пользователя по email {email}")


class GetResetEmailException(ServiceException):
    def __init__(
        self,
        message: str = RESET_EMAIL_FAILED,
        code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message=message, code=code)


class GetUserByIdException(ServiceException):
    def __init__(
        self,
        message: str = GET_USER_BY_ID_EXCEPTION,
        code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message=message, code=code)


class UserUpdateException(ServiceException):
    def __init__(
        self,
        message: str = GET_USER_BY_ID_EXCEPTION,
        code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message=message, code=code)


class GetAllFriendsException(ServiceException):
    def __init__(self, message: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message=message, code=code)


class GetFriendByIdException(ServiceException):
    def __init__(self, message: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message=message, code=code)


class GetAllItemsException(ServiceException):
    def __init__(self, message: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message=message, code=code)
