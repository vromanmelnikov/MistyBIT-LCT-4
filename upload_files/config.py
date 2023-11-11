from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CORS_URL: List[str]

    class Config:
        env_file = ".env"


settings = Settings()
