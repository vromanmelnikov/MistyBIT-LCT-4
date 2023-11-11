from abc import ABC, abstractmethod
from datetime import date, timedelta

from sqlalchemy import Float, Integer

from src.task.const import *
from src.task.schemas import OperatorSchema


class BaseOperator(ABC):
    def __init__(self, name: str, tag: str):
        self.name = name
        self.tag = tag

    def get_object(self):
        return OperatorSchema(name=self.name, tag=self.tag)

    @abstractmethod
    def execute(self, left_value, right_value):
        raise NotImplementedError()


class MoreOperator(BaseOperator):
    def __init__(self):
        super().__init__("$больше", LOGIC)

    def execute(self, left_value, right_value):
        return left_value > right_value


class MoreEqualOperator(BaseOperator):
    def __init__(self):
        super().__init__("$больше_или_равно", LOGIC)

    def execute(self, left_value, right_value):
        return left_value >= right_value


class LessOperator(BaseOperator):
    def __init__(self):
        super().__init__("$меньше", LOGIC)

    def execute(self, left_value, right_value):
        return left_value < right_value


class LessEqualOperator(BaseOperator):
    def __init__(self):
        super().__init__("$меньше_или_равно", LOGIC)

    def execute(self, left_value, right_value):
        return left_value <= right_value


class EqualOperator(BaseOperator):
    def __init__(self):
        super().__init__("$равно", LOGIC)

    def execute(self, left_value, right_value):
        return left_value == right_value


class NotEqualOperator(BaseOperator):
    def __init__(self):
        super().__init__("$не_равно", LOGIC)

    def execute(self, left_value, right_value):
        return left_value != right_value


class LessDayAgainOperator(BaseOperator):
    def __init__(self):
        super().__init__("$меньше_n_дней", DATE)

    def execute(self, left_value, right_value):
        d = date.today() - timedelta(days=right_value)
        return left_value < d


class MoreDayAfterOperator(BaseOperator):
    def __init__(self):
        super().__init__("$больше_n_дней", DATE)

    def execute(self, left_value, right_value):
        d = date.today() + timedelta(days=right_value)
        return left_value > d


class EqualDayAgainOperator(BaseOperator):
    def __init__(self):
        super().__init__("$ровно_n_дней_назад", DATE)

    def execute(self, left_value, right_value):
        d = date.today() - timedelta(days=right_value)
        return left_value == d


class EqualDayAfterOperator(BaseOperator):
    def __init__(self):
        super().__init__("$ровно_n_дней_вперед", DATE)

    def execute(self, left_value, right_value):
        d = date.today() + timedelta(days=right_value)
        return left_value == d


class SubtractionOperator(BaseOperator):
    def __init__(self):
        super().__init__("$вычитание", ARITHMETIC)

    def execute(self, left_value, right_value):
        return left_value.cast(Integer) - right_value.cast(Integer)


class AdditionOperator(BaseOperator):
    def __init__(self):
        super().__init__("$сложение", ARITHMETIC)

    def execute(self, left_value, right_value):
        return left_value.cast(Integer) + right_value.cast(Integer)


class MultiplyOperator(BaseOperator):
    def __init__(self):
        super().__init__("$умножение", ARITHMETIC)

    def execute(self, left_value, right_value):
        return left_value.cast(Integer) * right_value.cast(Integer)


class DivisionOperator(BaseOperator):
    def __init__(self):
        super().__init__("$деление", ARITHMETIC)

    def execute(self, left_value, right_value):
        return left_value.cast(Float) / right_value.cast(Float)
