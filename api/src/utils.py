from typing import Any, Callable, Annotated, get_args, get_origin
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.dependencies.utils import get_typed_signature
from fastapi_cache import default_key_builder

from src.exceptions import NotFoundException, ServiceException
from src.mappers import BaseMapper
from src.schemas.response_items import ResponseItemsSchema


class IncrementorId:
    def __init__(self):
        self.current_value = 0

    def get_value(self):
        self.current_value += 1
        return self.current_value


def check_count_items(items, phrase: str):
    l = len(items)
    if l == 0:
        raise NotFoundException(phrase)
    return l


def check_exist_items(item, phrase: str | None = None, exeption=NotFoundException):
    if item is None:
        if phrase:
            raise exeption(phrase)
        else:
            raise exeption()


def handle_service_exception(request: Request, exc: ServiceException):
    return JSONResponse(content={"detail": exc.message}, status_code=exc.code)


def process_items_from_database(
    items: list,
    phrase_not_found: str,
    mapper: BaseMapper,
    offset: int | None = None,
    is_resp_schema: bool = True,
):
    l = check_count_items(items, phrase_not_found)
    items_pr = [mapper.create_from_database(i) for i in items]
    if is_resp_schema:
        return ResponseItemsSchema.Of(items_pr, offset, l)
    return items_pr


def process_item_from_database(item, phrase_not_found: str, mapper: BaseMapper):
    check_exist_items(item, phrase_not_found)
    return mapper.create_from_database(item)


IgnoredArgCache = object()


def custom_key_builder(
    func: Callable[..., Any], namespace: str, *, kwargs: dict[str, Any], **kw: Any
) -> str:
    # ignore the task argument
    ignored = set()
    for param in get_typed_signature(func).parameters.items():
        ann = param[1].annotation
        if get_origin(ann) is Annotated and IgnoredArgCache in get_args(ann):
            kwargs.pop(param[0], None)
    return default_key_builder(func, namespace, kwargs=kwargs, **kw)
