from fastapi import Depends

from src.dependies import *
from src.services import *
from src.ws.service_note import NoteService


def create_note_service(uow: IUnitOfWork = Depends(create_uow)):
    return NoteService(uow)
