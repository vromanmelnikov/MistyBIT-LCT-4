from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel

Item = TypeVar("Item")


class ResponseItemsSchema(GenericModel, Generic[Item]):
    items: List[Item]
    count: int
    num_offset: int | None = None

    @staticmethod
    def Of(items, offset, length=None):
        return ResponseItemsSchema(
            items=items,
            count=length or len(items),
            num_offset=offset or None,
        )
