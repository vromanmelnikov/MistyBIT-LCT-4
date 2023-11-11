from src.utils import check_count_items
from src.schemas.response_items import ResponseItemsSchema
from src.database.models import Note
from src.schemas import MessageSchema
from src.services.unit_of_work import IUnitOfWork
from src.ws.phrases import *
from src.ws.schema import *
from src.database.exceptions import *
from src.exceptions import *


class NoteService:
    def __init__(self, uow: IUnitOfWork):
        self.__uow = uow

    async def post_note(self, note: NotePostSchema):
        async with self.__uow:
            try:
                note_db = Note(user_id=note.user_id, message=note.message)
                await self.__uow.notes.add(note_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_ADD_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def get_users_note(
        self, user_id: int, limit: int | None, offset: int | None
    ) -> ResponseItemsSchema[NoteSchema]:
        async with self.__uow:
            try:
                notes = await self.__uow.notes.get_all(offset, limit, user_id=user_id)
                l = check_count_items(notes, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [NoteSchema.from_orm(n) for n in notes], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e
