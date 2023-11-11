from fastapi import APIRouter, Depends, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

from src.authentication.constants import *
from src.authentication.dependies import create_authentication_service
from src.authentication.schemas import *
from src.authentication.service import AuthenticationService
from src.background_tasks.base import *
from src.schemas.message import MessageSchema

router = APIRouter(prefix=f"/{AUTH}", tags=["Auth"])
security = HTTPBearer()


@router.post(PATH_SIGNIN, response_model=TokenSchema, summary="Аутенфикация")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authentication_service: AuthenticationService = Depends(
        create_authentication_service
    ),
):
    token, email = await authentication_service.login(form_data)
    send_warn_signin.delay(email)
    return token


@router.post("/refresh_token", response_model=TokenSchema, summary="Обновление токена")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    authentication_service: AuthenticationService = Depends(
        create_authentication_service
    ),
):
    return authentication_service.refresh_token(credentials)


@router.post(
    "/password/recover", response_model=MessageSchema, summary="Востановление пароля"
)
async def recover_password(
    data: RecoverPasswordSchema,
    authentication_service: AuthenticationService = Depends(
        create_authentication_service
    ),
):
    message, url, email = await authentication_service.recover_password(data)
    send_url.delay(email, url)
    return message


@router.post("/password/reset", response_model=MessageSchema, summary="Сменить пароль")
async def reset_password(
    data: ResetPasswordSchema,
    authentication_service: AuthenticationService = Depends(
        create_authentication_service
    ),
):
    return await authentication_service.reset_password(data)
