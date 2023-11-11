from fastapi.security import OAuth2PasswordRequestForm
from src.authentication.schemas import *
from src.const import *
from src.user.schemas import *


class UserLoginMapper:
    def create_from_input(self, form_data: OAuth2PasswordRequestForm):
        return UserLoginSchema(email=form_data.username, password=form_data.password)


class PasswordRecoveryMapper:
    def create_from_database(self, value: bytes):
        return value.decode("utf-8")
