from fastapi import APIRouter, Depends, Request

from src.authorization.authorization import AuthorizationService
from src.authorization.const import *
from src.authorization.dependies import factory_default_auth
from src.authorization.schemas import ResourceData, UpdatePolicySchema
from src.config import OAuth2Scheme
from src.const import ALL


router = APIRouter(prefix=SECURITY_COMMON_URL, tags=["Secure"])


@router.get(f"{METHODS}{ALL}", summary="Получение всех защищенных методов системы")
async def get_methods_all(
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await authorization_service.get_all_methods()


@router.get(
    f"{POLICIES}{ALL}", summary="Получение политик безопасности защищенного метода"
)
async def get_policies_by_method(
    action: str,
    resource: str,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await authorization_service.get_all_policies(action, resource)


@router.put(f"{POLICIES}", summary="Изменение политик безопасности")
async def update_policy(
    data: UpdatePolicySchema,
    request: Request,
    token: str = Depends(OAuth2Scheme),
    authorization_service: AuthorizationService = Depends(factory_default_auth),
):
    await authorization_service.check_authorization(
        request.method.lower(), ResourceData(name=request.url.path), token
    )
    return await authorization_service.update_policy(data)
