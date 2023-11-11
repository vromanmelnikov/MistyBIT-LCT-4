from pydantic import BaseModel


class MessageSchema(BaseModel):
    mailer_result: str
