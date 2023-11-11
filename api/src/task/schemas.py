from pydantic import BaseModel, Field
from src.database.models import *
from src.task.const import MAX_VALUE_FEEDBACK, MIN_VALUE_FEEDBACK
from src.user.schemas import EmployeeSchema, GradeSchema, SkillSchema
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from datetime import datetime

from src.office.schemas import PointSchema


class OperatorSchema(BaseModel):
    name: str
    tag: str


class CreateConditionSchema(BaseModel):
    description: str
    formula: dict
    task_id: int


class UpdateConditionSchema(BaseModel):
    description: str
    formula: dict
    id: int


class PrioritySchema(sqlalchemy_to_pydantic(Priority)):
    class Config:
        from_attributes = True


class TypeTaskSchema(sqlalchemy_to_pydantic(TypeTask)):
    class Config:
        from_attributes = True


class TypeTaskPostSchema(BaseModel):
    name: str
    priority_id: int
    duration: float
    details: dict
    interval_block: int

    conditions: list


class TypeTaskPutSchema(TypeTaskPostSchema):
    id: int


class TypeTaskGradePostSchema(BaseModel):
    type_task_id: int
    grade_id: int


class TypeTaskSkillPostSchema(BaseModel):
    type_task_id: int
    skill_id: int


class TypeTaskGradeSchema(sqlalchemy_to_pydantic(TypeTaskGradeLink)):
    class Config:
        from_attributes = True


class TypeTaskGradeGetSchema(TypeTaskGradeSchema):
    grade: GradeSchema | None = None


class TypeTaskSkillSchema(sqlalchemy_to_pydantic(TypeTaskSkillLinks)):
    class Config:
        from_attributes = True


class TypeTaskSkillGetSchema(TypeTaskSkillSchema):
    skill: SkillSchema | None = None


class PrioritySchema(sqlalchemy_to_pydantic(Priority)):
    class Config:
        from_attributes = True


class ConditionSchema(sqlalchemy_to_pydantic(Condition)):
    class Config:
        from_attributes = True


class TypeTaskGetSchema(TypeTaskSchema):
    priority: PrioritySchema | None = None
    grade_links: list[TypeTaskGradeGetSchema] = []
    skill_links: list[TypeTaskSkillGetSchema] = []
    conditions: list[ConditionSchema] = []


class BlockTaskSchema(BaseModel):
    task_id: int
    point_id: int
    interval: int


class TaskSchema(sqlalchemy_to_pydantic(Task)):
    date_begin: datetime | None = None
    employee_id: int | None = None

    class Config:
        from_attributes = True


class TypeTaskGetForTaskSchema(TypeTaskSchema):
    grade_links: list[TypeTaskGradeGetSchema] = []
    skill_links: list[TypeTaskSkillGetSchema] = []


class TaskStatusSchema(sqlalchemy_to_pydantic(TaskStatus)):
    class Config:
        from_attributes = True


class TaskGetSchema(TaskSchema):
    type: TypeTaskGetForTaskSchema | None = None
    point: PointSchema | None = None
    priority: PrioritySchema | None = None
    status: TaskStatusSchema | None = None
    employee: EmployeeSchema | None = None


class TaskHistorySchema(sqlalchemy_to_pydantic(HistoryTask)):
    type: dict | None = None
    type_id: int | None = None
    point: dict | None = None
    point_id: int | None = None
    status_id: int | None = None
    employee: dict | None = None
    employee_id: int | None = None
    feedback_value: int | None = None
    feedback_description: str | None = None

    date_begin: datetime | None = None
    date_create: datetime | None = None

    class Config:
        from_attributes = True


class TaskCompletedSchema(BaseModel):
    id: int
    feedback_value: int | None = Field(
        default=None, min_value=MIN_VALUE_FEEDBACK, max_value=MAX_VALUE_FEEDBACK
    )
    feedback_description: str | None = None


class TaskCancelledSchema(BaseModel):
    id: int
    feedback_description: str | None = None



