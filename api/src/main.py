from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi.openapi.utils import get_openapi

from src.authorization.config import init_default_policies
from src.config import *
from src.exceptions import ServiceException
from src.const import *
from src.routers import Routers
from src.utils import *
from src.authorization.dependies import *



@asynccontextmanager
async def lifespan(app: FastAPI):
    SchemaAPI(get_openapi(title=BACKEND_NAME, version=VERSION, routes=app.routes))
    await init_default_policies()
    print("Запуск...")
    yield
    FastAPICache.reset()


app = FastAPI(title=BACKEND_NAME, version=VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_URL,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(ServiceException, handle_service_exception)


for router in Routers:
    app.include_router(router)
