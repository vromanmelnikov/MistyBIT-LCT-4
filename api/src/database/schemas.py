from typing import Any
from pydantic import BaseModel


class RecordRedisSchema(BaseModel):
    key: str
    value: Any
    expire: int=0
