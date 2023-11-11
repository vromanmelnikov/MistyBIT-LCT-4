from typing import List
from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from redis import Redis, asyncio as aioredis
from celery import Celery

from src.authentication.constants import *
from src.const import *
from src.ws.service import WebsocketConnectionService


# environment
class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    HOST: str
    PORT: str

    SECRET_STRING: str
    ALGORITHM: str

    CORS_URL: List[str]
    URL_ME: str
    URL_MAILER: str
    URL_FRONTEND: str
    URL_UPLOAD_FILE: str

    REDIS_HOST: str
    REDIS_PORT: str

    YANDEX_KEY_API_LOC: str
    YANDEX_URL: str
    YANDEX_TRAFFIC_URL: str

    OSRM_API: str

    class Config:
        env_file = ".env"


settings = Settings()

# authorization
OAuth2Scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH}{PATH_SIGNIN}")

# connections
REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
RedisConnection = aioredis.from_url(REDIS_URL, encoding="utf8")
SyncRedisConnection = Redis(settings.REDIS_HOST, settings.REDIS_PORT)
CeleryConnection = Celery(MAIN_QUEUE_NAME_CELERY, broker=REDIS_URL)


class OpenAPISchemaStore:
    def __init__(self):
        self.schema = {}

    def __call__(self, schema):
        self.schema = schema


SchemaAPI = OpenAPISchemaStore()
NoteWebsockerConnection = WebsocketConnectionService()
