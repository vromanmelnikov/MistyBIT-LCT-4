from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from src.database.models.task.note import Note


class WSMessageSchema(BaseModel):
    message: str
    code: int


class NotePostSchema(BaseModel):
    user_id: int
    message: str


class NoteSchema(sqlalchemy_to_pydantic(Note)):
    class Config:
        from_attributes = True


hello_message = WSMessageSchema(message="OK", code=200)
