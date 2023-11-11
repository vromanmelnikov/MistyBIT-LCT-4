from fastapi import APIRouter, Depends, File, Request, UploadFile, Query
from src.authorization.schemas import ResourceData

from src.const import DEFAULT_LIMIT, VALUE_NOT_LESS, DEFAULT_OFFSET
from src.office.const import *
from src.office.dependencies import create_office_service
from src.office.service import OfficeService
from src.office.schemas import *
from src.schemas.response_items import ResponseItemsSchema
from src.config import OAuth2Scheme
from src.authorization.authorization import AuthorizationService
from src.authorization.dependies import factory_default_auth
from src.const import *


router = APIRouter(prefix=COMMON_URL, tags=["Offices"])


@router.get(
    "/count_weights",
    summary="Подсчет весов каждой ветки и трафика (НЕ ТРОГАТЬ!!!!!!!!!!!!!!!!!!!!)",
)
async def count_weights(
    count_remains: bool = Query(default=False, description="True если нужно обновить веса только что добавленных объектов"),
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.count_weights(count_remains)


@router.get(
    ALL,
    response_model=ResponseItemsSchema[OfficeSchema],
    summary="Получение всех офисов",
)
async def get_offices(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво офисов",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    substr: str = Query(default=None, description="Подстрока адреса офиса"),
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.get_offices(limit, offset, substr)


@router.get("/{id}", summary="Получение конкретного офиса")
async def get_office(
    id: int,
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.get_by_id(id)


@router.post("/", summary="Добавление офиса")
async def add_office(
    request: Request,
    office: OfficePostSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.post_office(office)


@router.put(
    "/", summary="Изменение офиса (если coordinate не заполнено, берется из АПИ)"
)
async def update_office(
    request: Request,
    office: OfficePutSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.put_office(office)


@router.post(IMMAGE, summary="Добавление картинки для офиса")
async def post_officeimage(
    request: Request,
    id: int,
    file: UploadFile = File(...),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.post_image_office(id, file)


@router.post(f"{POINTS}{IMMAGE}", summary="Добавление картинки для точки")
async def post_pointimage(
    request: Request,
    id: int,
    file: UploadFile = File(...),
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.post_image_point(id, file)


@router.delete("/", summary="Удаление офиса")
async def delete_office(
    request: Request,
    id: int,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.delete_office(id)


@router.post(f"{POINTS}", summary="Добавление точки")
async def post_point(
    request: Request,
    point: PointPostSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.post_point(point)


@router.put(
    f"{POINTS}",
    summary="Изменение точек (адреса) (если coordinate не заполнено, берется из АПИ)",
)
async def put_point(
    request: Request,
    point: PointPutSchema,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.put_point(point)


@router.delete(f"{POINTS}", summary="Удаление точки")
async def delete_point(
    request: Request,
    id: int,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
    office_service: OfficeService = Depends(create_office_service),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await office_service.delete_point(id)


@router.put(f"{POINTS}/is_delivered_card", summary="Привезли карточки")
async def put_point_is_delivered_card(
    id: int,
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.put_point_is_delivered_card(id)


@router.put(f"{POINTS}/quantity_requests", summary="Добавление заявок точке")
async def put_quantity_requests(
    id: int,
    number: int = Query(ge=1),
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.put_quantity_requests(id, number)


@router.put(f"{POINTS}/quantity_card", summary="Добавление карточек точке")
async def put_quantity_card(
    id: int,
    number: int = Query(ge=1),
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.put_quantity_card(id, number)


@router.get(
    f"{POINTS}/",
    response_model=ResponseItemsSchema[PointSchema],
    summary="Получение всех точек",
)
async def get_points(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=VALUE_NOT_LESS,
        le=DEFAULT_LIMIT,
        description="Колво точек",
    ),
    offset: int = Query(
        default=DEFAULT_OFFSET, ge=VALUE_NOT_LESS, description="Смещение"
    ),
    substr: str = Query(default=None, description="Подстрока адреса точки"),
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.get_points(limit, offset, substr)


@router.get(
    f"{POINTS}{COLUMNS}",
    response_model=list[DictPointSchema],
    summary="Вывод полезных полей точки",
)
async def get_dict_point(
    office_service: OfficeService = Depends(create_office_service),
):
    return await office_service.get_dict_point()
