from src.exceptions import BaseAppException


class DBException(BaseAppException):
    """Базовое исключение для репозиториев"""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidColumnException(DBException):
    """Неизвестный столбец для фильтрации"""

    def __init__(self, column: str):
        super().__init__(f"Неверное название столбца {0}".format(column))


class GetAllItemsException(DBException):
    """Ошибка получения всех элементов"""

    def __init__(self, table: str):
        super().__init__(f"Не удалось получить элементы из таблицы {table}")


class GetOneItemException(DBException):
    """Ошибка получения элемента"""

    def __init__(self, table: str):
        super().__init__(f"Не удалось получить элемент из таблицы {table}")


class GetItemByIdException(DBException):
    """Ошибка получения элемента по id"""

    def __init__(self, table: str, id: int):
        super().__init__(f"Не удалось получить элемент из таблицы {table} по id {id}")


class UniqueViolationException(DBException):
    """Ошибка уникальности поля"""

    def __init__(self, value: str):
        super().__init__(f"Значение '{value}' не уникально")


class ForeignKeyViolationException(DBException):
    """Ошибка внешнего ключа"""

    def __init__(self, table: str):
        super().__init__(
            f"Элемент, на который указывает внешний ключ в таблице '{table}' отсутствует"
        )


class AddItemException(DBException):
    """Ошибка добавления элемента"""

    def __init__(self, table: str | None = None):
        super().__init__(
            f"Не удалось добавить элемент{' в таблицу ' if table else ''}{table if table else ''}"
        )


class UpdateItemException(DBException):
    """Ошибка изменения элемента"""

    def __init__(self, table: str):
        super().__init__(f"Не удалось изменить элемент в таблице {table}")


class DeleteItemException(DBException):
    """Ошибка удаления элемента"""

    def __init__(self, table: str):
        super().__init__(f"Не удалось удалить элемент из таблицы '{table}")
