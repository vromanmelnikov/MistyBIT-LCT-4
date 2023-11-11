from fastapi import (
    APIRouter,
    Depends,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    Header,
)

from src.authentication.constants import ACCESS_TOKEN
from src.authentication.dependies import create_authentication_service
from src.authentication.service import AuthenticationService
from src.authorization.authorization import AuthorizationService
from src.authorization.schemas import ResourceData
from src.const import *
from src.ws.dependencies import create_note_service
from src.ws.schema import hello_message
from src.config import NoteWebsockerConnection, OAuth2Scheme
from src.exceptions import ServiceException
from src.ws.service_note import NoteService
from src.authorization.dependies import factory_default_auth

router = APIRouter(tags=["Note"], prefix="/notifications")


@router.get("/", summary="Получение своих уведомлений")
async def get_notifications(
    request: Request,
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво уведомлений",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    note_service: NoteService = Depends(create_note_service),
):
    resource_data, subject_data = await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await note_service.get_users_note(subject_data.id, limit, offset)


@router.websocket("/tg-ws")
async def websocket_endpoint(
    websocket: WebSocket,
    auth_service: AuthenticationService = Depends(create_authentication_service),
):
    await NoteWebsockerConnection.tg_connect(websocket)
    await NoteWebsockerConnection.tg_send_msg(hello_message.dict())
    try:
        while True:
            data = await websocket.receive_json()
            token = data["token"]
            chat_id = data["chat_id"]

            try:
                token_data = auth_service.decode_token(token, ACCESS_TOKEN)
                NoteWebsockerConnection.tg_add_user(token_data.id, chat_id)
                await NoteWebsockerConnection.tg_send_msg({"code": 200})
            except ServiceException as e:
                await NoteWebsockerConnection.tg_send_msg(
                    {"code": e.code, "message": e.message}
                )

    except WebSocketDisconnect:
        NoteWebsockerConnection.tg_disconnect()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_key: str,
    token: str,
    auth_service: AuthenticationService = Depends(create_authentication_service),
):
    try:
        token_data = auth_service.decode_token(token, ACCESS_TOKEN)
    except ServiceException as e:
        return {"code": e.code, "message": e.message}
    if token_data.id and client_key:
        await NoteWebsockerConnection.connect(websocket, token_data.id, client_key)
        await NoteWebsockerConnection.send_personal_message_to_device(
            hello_message.dict(), token_data.id, client_key
        )
        try:
            while True:
                data = await websocket.receive_json()
                await NoteWebsockerConnection.send_personal_message(data, token_data.id)
        except WebSocketDisconnect:
            NoteWebsockerConnection.disconnect(token_data.id, client_key)
