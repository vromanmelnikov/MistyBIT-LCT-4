from fastapi import status

from src.phrases import ANY_EXCEPTIONS


class BaseAppException(Exception):
    def __init__(self, message: str):
        self.message = message


class ServiceException(BaseAppException):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


class AnyServiceException(ServiceException):
    def __init__(self, message: str = ANY_EXCEPTIONS):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotFoundException(ServiceException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class BadRequestException(ServiceException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
