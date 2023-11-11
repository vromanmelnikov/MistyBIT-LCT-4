from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EMAIL_SENDER: EmailStr
    PASSWORD: str
    LOGO_URL: str
    SMTP_PORT_SSL: int
    PATH_TEMPLATE: str

    class Config:
        env_file = ".env"


settings = Settings()
