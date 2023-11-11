import secrets
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from pydantic import ValidationError
from passlib.context import CryptContext
import jwt
from jose import JWTError
from datetime import datetime, timedelta

from src.authentication.constants import *
from src.authentication.exceptions import *
from src.authentication.mappers import *
from src.authentication.phrases import *
from src.authentication.schemas import *
from src.const import *
from src.database.exceptions import *
from src.exceptions import AnyServiceException, BadRequestException
from src.mappers import RecordRedisMapper
from src.schemas import *
from src.config import settings
from src.services.unit_of_work import IUnitOfWork
from src.user.exceptions import GetUserByEmailException


class AuthenticationService:
    def __init__(self, uow: IUnitOfWork):
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__uow = uow

    def refresh_token(self, credentials: HTTPAuthorizationCredentials):
        data = self.decode_token(credentials.credentials, REFRESH_TOKEN)
        return self.__generate_tokens(data)

    async def login(self, form_data: OAuth2PasswordRequestForm):
        async with self.__uow:
            try:
                user_login = UserLoginMapper().create_from_input(form_data)
                user_db = await self.check_exist_user(
                    user_login.email, self.__uow, False
                )

                if user_db is None:
                    raise AuthException(INVALID_USERNAME) from None
                if not user_db.is_active:
                    raise AuthException(IS_NOT_ACTIVE) from None
                if not self.__verify_password(
                    form_data.password, user_db.hashed_password
                ):
                    raise AuthException(INVALID_PASSWORD) from None
                return (
                    self.__generate_tokens(
                        TokenDataSchema.Of(user_db.id, user_db.role_id)
                    ),
                    user_db.email,
                )
            except GetUserByEmailException as e:
                raise AuthException(e.message) from e
            except ValidationError:
                raise BadRequestException(INCORRECT_EMAIL)

    async def reset_password(self, data: ResetPasswordSchema):
        async with self.__uow:
            record = await self.__uow.pswd_recoveries.pop(data.code)
            if record:
                email = PasswordRecoveryMapper().create_from_database(record)
                user = await self.check_exist_user(email, self.__uow, False)
                user.hashed_password = self.get_password_hash(data.password)
                user.is_active = True
                await self.__uow.commit()
                return MessageSchema(message=PASSWORD_SUCCESS_RESET)
            raise BadRequestException(CODE_INVALID)

    async def recover_password(
        self, data: RecoverPasswordSchema, time: int = EXPIRES_10_MIN_CACHE_ON_SECONDS
    ):
        async with self.__uow:
            try:
                await self.check_exist_user(data.email, self.__uow, False)
                key = secrets.token_urlsafe(16)
                record = RecordRedisMapper().create_from_input(key, data.email, time)
                if await self.__uow.pswd_recoveries.add(record):
                    return (
                        MessageSchema(message=URL_SEND_SUCCESS),
                        f"{settings.URL_FRONTEND}/auth/reset?code={key}",
                        data.email,
                    )
                raise BadRequestException(CODE_SEND_FAILED)
            except AddItemException as e:
                raise AnyServiceException(CODE_SEND_FAILED) from e

    def decode_token(self, token: str, scope: str) -> TokenDataSchema:
        try:
            payload = jwt.decode(
                token, settings.SECRET_STRING, algorithms=[settings.ALGORITHM]
            )
            if payload[PAYLOAD_NAME_SCOPE] == scope:
                user_id = payload.get(PAYLOAD_NAME_SUB_ID)
                role_id = payload.get(PAYLOAD_NAME_SUB_ROLE_ID)
                if user_id and role_id:
                    return TokenDataSchema.Of(user_id, role_id)
                raise AuthException(COULD_NOT_VALIDATE) from None
            raise AuthException(TOKEN_INVALID_SCOPE) from None

        except jwt.ExpiredSignatureError:
            raise AuthException(TOKEN_EXPIRED) from None
        except jwt.InvalidTokenError:
            raise AuthException(TOKEN_INVALID_SCOPE) from None
        except (JWTError, ValidationError):
            raise AuthException(COULD_NOT_VALIDATE) from None

    async def check_exist_user(
        self, email: str, uow: IUnitOfWork, exist_error: bool = True
    ):
        try:
            user = await uow.users.get_by_login(email)
            if user:
                if exist_error:
                    raise BadRequestException(EMAIL_ALREADY_EXIST)
                return user
            elif not exist_error:
                raise AuthException(INVALID_USERNAME)
        except GetUserByEmailException as e:
            raise AnyServiceException(CHECK_EXIST)

    def get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    def __verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

    def __generate_tokens(self, data: TokenDataSchema):
        access_payload = self.__constructor_payload(
            data, timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES), ACCESS_TOKEN
        )
        refresh_payload = self.__constructor_payload(
            data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), REFRESH_TOKEN
        )
        access_token = self.__generate_token(access_payload)
        refresh_token = self.__generate_token(refresh_payload)
        return TokenSchema.Of(access_token, refresh_token)

    def __generate_token(self, payload):
        return jwt.encode(payload, settings.SECRET_STRING, algorithm=settings.ALGORITHM)

    def __constructor_payload(
        self, data: TokenDataSchema, expires: timedelta, scope: str
    ):
        payload = {
            PAYLOAD_NAME_SCOPE: scope,
            PAYLOAD_NAME_SUB_ID: data.id,
            PAYLOAD_NAME_SUB_ROLE_ID: data.role_id,
            PAYLOAD_NAME_EXPIRES: datetime.utcnow() + expires,
            PAYLOAD_NAME_ISSUEDAT: datetime.utcnow(),
        }
        return payload
