from src.authentication.router import router as authentication_router
from src.task.router import router as task_router
from src.office.router import router as office_router
from src.user.router import router as user_router
from src.authorization.router import router as authorization_router
from src.ws.router import router as note_router

Routers = [
    authentication_router,
    task_router,
    office_router,
    user_router,
    authorization_router,
    note_router,
]
