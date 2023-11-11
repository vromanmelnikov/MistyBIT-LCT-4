from io import BytesIO
import json
import random
import xlsxwriter
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, inspect, select, or_
from datetime import datetime
from src.authorization.schemas import SubjectData

from src.database.exceptions import *
from src.schemas.response_items import ResponseItemsSchema
from src.services.unit_of_work import IUnitOfWork
from src.task.const import *
from src.task.operators import BaseOperator
from src.task.schemas import *
from src.task.special_actions import SpecialActionBase
from src.utils import *
from src.task.phrases import *
from src.schemas.message import MessageSchema
from src.exceptions import *


class TaskService:
    def __init__(
        self,
        uow: IUnitOfWork,
        operators: list[BaseOperator],
        special_actions: list[SpecialActionBase],
    ):
        self.__uow = uow
        self.__special_actions = special_actions
        self.__operators = {o.get_object().name: o for o in operators}

    async def get_all_tasks(
        self,
        limit: int | None,
        offset: int | None,
        type_id: int | None,
        point_id: int | None,
        status_id: int | None,
        priority_id: int | None,
        employee_id: int | None,
        date_create: datetime | None,
        date_begin: datetime | None,
        to_all: bool = True,
    ) -> ResponseItemsSchema[TaskGetSchema]:
        async with self.__uow:
            try:
                tasks = await self.__uow.tasks.get_all_full_front(
                    limit,
                    offset,
                    type_id,
                    point_id,
                    status_id,
                    priority_id,
                    employee_id,
                    date_create,
                    date_begin,
                    to_all,
                )
                l = check_count_items(tasks, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [TaskGetSchema.from_orm(t) for t in tasks], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def get_report(self):
        async with self.__uow:
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)
            tasks_db = await self.__uow.tasks.get_all_full_front(
                None, None, None, None, None, None, None, None, None
            )
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "Наименование")
            worksheet.write(0, 1, "Адрес")
            worksheet.write(0, 2, "Статус")
            worksheet.write(0, 3, "Сотрудник")
            worksheet.write(0, 4, "Грейд")
            worksheet.write(0, 5, "Офис")
            worksheet.write(0, 6, "Дата создания")
            worksheet.write(0, 7, "Дата принятия")
            for i in range(len(tasks_db)):
                worksheet.write(i + 1, 0, tasks_db[i].type.name)
                worksheet.write(i + 1, 1, tasks_db[i].point.address)
                worksheet.write(i + 1, 2, tasks_db[i].status.name)
                fullname = ""
                if tasks_db[i].employee is not None:
                    fullname = f"{tasks_db[i].employee.user.lastname} {tasks_db[i].employee.user.firstname} {tasks_db[i].employee.user.patronymic}"
                worksheet.write(i + 1, 3, fullname)
                worksheet.write(
                    i + 1,
                    4,
                    tasks_db[i].employee.grade.name
                    if tasks_db[i].employee is not None
                    else "",
                )
                worksheet.write(
                    i + 1,
                    5,
                    tasks_db[i].employee.office.address
                    if tasks_db[i].employee is not None
                    else "",
                )
                worksheet.write(
                    i + 1, 6, tasks_db[i].date_create.strftime("%d-%b-%Y-%H:%M:%S")
                )
                worksheet.write(
                    i + 1,
                    7,
                    tasks_db[i].date_begin.strftime("%d-%b-%Y-%H:%M:%S")
                    if tasks_db[i].date_begin is not None
                    else "",
                )

            worksheet.autofit()

            workbook.close()
            output.seek(0)
            date_now = datetime.now().strftime("%d-%b-%Y-%H:%M:%S")
            headers = {
                "Content-Disposition": f'attachment; filename="statistic-{date_now}.xlsx"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            }
            return StreamingResponse(
                output, headers=headers, media_type="application/xls"
            )

    async def get_history_task(
        self, limit: int | None, offset: int | None, employee_id: int | None
    ) -> ResponseItemsSchema[TaskHistorySchema]:
        async with self.__uow:
            try:
                history_tasks = await self.__uow.history_tasks.get_all(
                    limit, offset, employee_id
                )
                l = check_count_items(history_tasks, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [TaskHistorySchema.from_orm(t) for t in history_tasks], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def put_task_by_manager(self, id: int, employee_id: int):
        async with self.__uow:
            try:
                task_db = await self.__uow.tasks.get_by_id(id)
                check_exist_items(task_db, OBJECT_NOT_FOUND)
                task_db.employee_id = employee_id
                task_db.status_id = STATUS_ID_APPOINTED
                await self.__uow.tasks.add(task_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_UPDATE_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def task_cancelled(
        self, task: TaskCancelledSchema, subject_data: SubjectData
    ):
        async with self.__uow:
            try:
                task_db = await self.__uow.tasks.get_by_id(task.id)
                check_exist_items(task_db, OBJECT_NOT_FOUND)
                history_task_db = await self._create_task_for_history(
                    task_db, STATUS_ID_CANCELLED, None, task.feedback_description
                )
                history_task_db = await self.__uow.history_tasks.add(history_task_db)
                await self.__uow.tasks.delete(id=task.id)

                msgs = []
                await self.__uow.commit()

                if subject_data.id == history_task_db.employee_id:
                    managers = await self.__uow.managers.get_all()
                    msg = 'Задача "{0}" отменена сотрудником {1} {2} {3} по причине {4}'.format(
                        history_task_db.type["name"],
                        history_task_db.employee["id"]["lastname"],
                        history_task_db.employee["id"]["firstname"],
                        history_task_db.employee["id"]["patronymic"],
                        task.feedback_description,
                    )
                    for m in managers:
                        msgs.append({"id": m.id, "msg": msg, "email": m.user.email})
                elif history_task_db.employee_id:
                    msg = 'Ваша задача "{0}" отменена по причине {1}'.format(
                        history_task_db.type["name"], task.feedback_description
                    )
                    msgs.append(
                        {
                            "id": history_task_db.employee_id,
                            "msg": msg,
                            "email": history_task_db.employee["id"]["email"],
                        }
                    )

                return MessageSchema(message=TASK_PROCESSED_SUCCESS), msgs
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_DELETE_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_DELETE_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def task_completed(
        self, data: TaskCompletedSchema, subject_data: SubjectData
    ):
        async with self.__uow:
            try:
                task_db = await self.__uow.tasks.get_by_id(data.id)
                check_exist_items(task_db, OBJECT_NOT_FOUND)
                history_task_db = await self._create_task_for_history(
                    task_db,
                    STATUS_ID_COMPLETED,
                    data.feedback_value,
                    data.feedback_description,
                )
                await self.__uow.history_tasks.add(history_task_db)
                await self.__uow.tasks.delete(id=data.id)
                for a in self.__special_actions:
                    await a.execute(
                        task_db.type_id, self.__uow, point_id=task_db.point_id
                    )
                await self.__uow.commit()
                msgs = []

                if subject_data.id == history_task_db.employee_id:
                    managers = await self.__uow.managers.get_all()
                    msg = 'Задача "{0}" выполнена сотрудником {1} {2} {3}. Отзыв: {4}'.format(
                        history_task_db.type["name"],
                        history_task_db.employee["id"]["lastname"],
                        history_task_db.employee["id"]["firstname"],
                        history_task_db.employee["id"]["patronymic"],
                        data.feedback_description,
                    )
                    for m in managers:
                        msgs.append({"id": m.id, "msg": msg, "email": m.user.email})

                elif history_task_db.employee_id:
                    msg = 'Ваша задача "{0}" отменена по причине {1}'.format(
                        history_task_db.type["name"], data.feedback_description
                    )
                    msgs.append(
                        {
                            "id": history_task_db.employee_id,
                            "msg": msg,
                            "email": history_task_db.employee["id"]["email"],
                        }
                    )

                return MessageSchema(message=TASK_PROCESSED_SUCCESS), msgs
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_DELETE_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_DELETE_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def accept_task(self, task_id: int):
        async with self.__uow:
            task_db = await self.__uow.tasks.get_by_id(task_id)
            check_exist_items(task_db, OBJECT_NOT_FOUND)
            task_db.status_id = STATUS_ID_ACCEPTED
            await self.__uow.commit()
            return MessageSchema(message=TASK_ACCEPTED)

    async def task_change_priority(self):
        async with self.__uow:
            tasks_db = await self.__uow.tasks.get_all()
            for t in tasks_db:
                t.priority_id = PRIORITY_ID_VERY_HIGH
            await self.__uow.commit()
            return MessageSchema(message=TASKS_UPDATED_SUCCESS)

    async def get_all_operators(self) -> ResponseItemsSchema[OperatorSchema]:
        return ResponseItemsSchema.Of(
            [o.get_object() for o in self.__operators.values()],
            None,
            len(self.__operators),
        )

    async def get_all_statuses(
        self, in_history: bool
    ) -> ResponseItemsSchema[TaskStatusSchema]:
        async with self.__uow:
            try:
                statuses = await self.__uow.task_statuses.get_all(in_history=in_history)
                l = check_count_items(statuses, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [TaskStatusSchema.from_orm(p) for p in statuses], None, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def get_all_priorities(self) -> ResponseItemsSchema[PrioritySchema]:
        async with self.__uow:
            try:
                priorities = await self.__uow.priorities.get_all()
                l = check_count_items(priorities, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [PrioritySchema.from_orm(p) for p in priorities], None, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def post_type_task(self, task: TypeTaskPostSchema):
        async with self.__uow:
            try:
                conditions = []
                for c in task.conditions:
                    select(Point).where(self.parse_condition(c["formula"]))
                    c_db = Condition(description=c["description"], formula=c["formula"])
                    conditions.append(c_db)
                task_db = TypeTask(
                    name=task.name,
                    priority_id=task.priority_id,
                    duration=task.duration,
                    details=task.details,
                    interval_block=task.interval_block,
                    conditions=conditions,
                )
                record = await self.__uow.type_tasks.add(task_db)
                id_rec = record.id
                await self.__uow.commit()
                return {"message": id_rec}
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e
            except Exception as e:
                raise BadRequestException(CONDITION_INVALID) from e

    async def put_type_task(self, task: TypeTaskPutSchema):
        async with self.__uow:
            try:
                task_db = await self.__uow.type_tasks.get_by_id(task.id)
                check_exist_items(task_db, OBJECT_NOT_FOUND)
                task_db.name = task.name
                task_db.priority_id = task.priority_id
                task_db.duration = task.duration
                task_db.details = task.details
                task_db.interval_block = task.interval_block
                await self.__uow.type_tasks.add(task_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_UPDATE_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def delete_type_task(self, id: int):
        async with self.__uow:
            try:
                task_exist = await self.__uow.type_tasks.get_by_id(id)
                check_exist_items(task_exist, OBJECT_NOT_FOUND)
                await self.__uow.type_tasks.delete(id=id)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def post_type_task_grade(self, task: TypeTaskGradePostSchema):
        async with self.__uow:
            try:
                type_task_grade_db = TypeTaskGradeLink(
                    type_task_id=task.type_task_id, grade_id=task.grade_id
                )
                await self.__uow.type_task_grades.add(type_task_grade_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_ADD_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def delete_type_task_grade(self, task: TypeTaskGradePostSchema):
        async with self.__uow:
            try:
                task_exist = await self.__uow.type_task_grades.get_one(
                    type_task_id=task.type_task_id, grade_id=task.grade_id
                )
                check_exist_items(task_exist, OBJECT_NOT_FOUND)
                await self.__uow.type_task_grades.delete(
                    type_task_id=task.type_task_id, grade_id=task.grade_id
                )
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def post_type_task_skill(self, task: TypeTaskSkillPostSchema):
        async with self.__uow:
            try:
                type_task_skill_db = TypeTaskSkillLinks(
                    type_task_id=task.type_task_id, skill_id=task.skill_id
                )
                await self.__uow.type_task_skills.add(type_task_skill_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_ADD_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_ADD_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e

    async def delete_type_task_skill(self, task: TypeTaskSkillPostSchema):
        async with self.__uow:
            try:
                task_exist = await self.__uow.type_task_skills.get_one(
                    type_task_id=task.type_task_id, skill_id=task.skill_id
                )
                check_exist_items(task_exist, OBJECT_NOT_FOUND)
                await self.__uow.type_task_skills.delete(
                    type_task_id=task.type_task_id, skill_id=task.skill_id
                )
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def get_all_type_tasks(self) -> ResponseItemsSchema[TypeTaskGetSchema]:
        async with self.__uow:
            try:
                type_tasks = await self.__uow.type_tasks.get_all_full()
                l = check_count_items(type_tasks, OBJECTS_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [TypeTaskGetSchema.from_orm(t) for t in type_tasks], None, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    def parse_condition(self, condition: dict):
        cs = []
        for key, value in condition.items():
            if key.startswith(SPEC_SYMBOL):
                v1 = Point.__dict__[value[f"{SPEC_SYMBOL}арг1"]]
                v2 = Point.__dict__[value[f"{SPEC_SYMBOL}арг2"]]
                o = self.__operators.get(key, None)
                if o:
                    exp = o.execute(v1, v2)

            else:
                exp = Point.__dict__[key]
            if isinstance(value, dict):
                for op, val in value.items():
                    o = self.__operators.get(op, None)
                    if o:
                        res = o.execute(exp, val)
                        cs.append(res)
            else:
                cs.append(exp == value)
        if len(cs) == 1:
            return cs[0]
        elif len(cs) > 1:
            return and_(*cs)

    def parse_formula(self, conditions: dict):
        stmt = select(Point)
        cs = []
        for c in conditions:
            cs.append(self.parse_condition(c))
        if len(cs) == 1:
            stmt = stmt.where(cs[0])
        elif len(cs) > 1:
            stmt = stmt.where(or_(*cs))

        return stmt

    async def post_task_conditions(self, data: CreateConditionSchema):
        async with self.__uow:
            try:
                # fields = await self.__office_service.get_dict_point()
                # fields = {field.ru: field.en for field in fields}
                # f = self.__proccess_formula(data.formula, fields)
                select(Point).where(self.parse_condition(data.formula))

                c = Condition(
                    type_task_id=data.task_id,
                    formula=data.formula,
                    description=data.description,
                )
                await self.__uow.task_conditions.add(c)
                await self.__uow.commit()
                return MessageSchema(message=CONDITION_POST_SUCCESS)
            except Exception as e:
                raise BadRequestException(CONDITION_INVALID) from e

    async def delete_task_conditions(self, condition_id: int):
        async with self.__uow:
            try:
                condition = await self.__uow.task_conditions.get_by_id(condition_id)
                check_exist_items(condition, OBJECT_NOT_FOUND)
                await self.__uow.task_conditions.delete(id=condition_id)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OBJECT_DELETE_FAILED) from e

    async def put_task_conditions(self, condition: UpdateConditionSchema):
        async with self.__uow:
            try:
                condition_db = await self.__uow.task_conditions.get_by_id(condition.id)
                check_exist_items(condition_db, OBJECT_NOT_FOUND)
                select(Point).where(self.parse_condition(condition.formula))
                condition_db.description = condition_db.description
                condition_db.formula = condition.formula
                await self.__uow.task_conditions.add(condition_db)
                await self.__uow.commit()
                return MessageSchema(message=OBJECT_UPDATE_SUCCESS)
            except UniqueViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except ForeignKeyViolationException as e:
                raise BadRequestException(message=OBJECT_UPDATE_FAILED) from e
            except AddItemException as e:
                raise AnyServiceException(message=OBJECT_ADD_FAILED) from e
            except Exception as e:
                raise BadRequestException(OBJECT_UPDATE_FAILED) from e

    async def define_tasks(self):
        async with self.__uow:
            try:
                type_tasks = await self.__uow.type_tasks.get_all_full()
                ids = []
                tasks = []
                for type_t in type_tasks:
                    conditions = [t.formula for t in type_t.conditions]
                    if len(conditions) == 0:
                        continue

                    stmt = self.parse_formula(conditions).where(
                        Point.id.not_in(ids),
                        Point.id.not_in(select(Task.point_id).subquery()),
                    )
                    new_points = await self.__uow.points.execute_stmt_all(stmt)
                    for p in new_points:
                        flag = await self.__uow.block_tasks.get_by_id(type_t.id, p.id)
                        if not flag:
                            task = Task(
                                type_id=type_t.id,
                                point_id=p.id,
                                status_id=IN_QUEUE_ID,
                                priority_id=type_t.priority_id,
                            )
                            tasks.append(task)
                            ids.append(p.id)
                await self.__uow.tasks.add_all(tasks)
                await self.__uow.commit()
                return MessageSchema(message=TASKS_DEFINED)
            except AddItemException as e:
                raise AnyServiceException(e) from e

    async def delete_tasks(self):
        async with self.__uow:
            try:
                await self.__uow.tasks.delete_all()
                await self.__uow.commit()
                return MessageSchema(message=TASK_DELETED_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=TASK_DELETED_FAILED) from e

    def __calc_skill_ratio(self, employee: dict, task: dict):
        task_skill_len = len(task["skills"])
        match_len = len(employee["skills"].intersection(task["skills"]))
        return task_skill_len / match_len if match_len > 0 else match_len

    def __calculate_match(
        self, employee: dict, task: dict, grades: dict, std_dur_go: int
    ):
        skill_ratio = self.__calc_skill_ratio(employee, task)
        e_grade = employee["grade"]
        min_grade = e_grade
        for g in task["grades"]:
            if g["value"] < min_grade["value"]:
                min_grade = g

        t_id = min_grade["id"]
        e_id = e_grade["id"]
        grade_ratio = grades[e_id][t_id]
        all_ratio = (
            task["duration_std"] * TASK_DURATION_RATIO
            + skill_ratio * SKILL_RATIO
            + std_dur_go * GO_DURATION_RATIO
            + grade_ratio * GRADE_RATIO
            + task["priority_value_std"] * PRIORITY_RATIO
        )
        return all_ratio

    def __calc_duration(
        self, task: dict, employee: dict, traffics: dict, durations: dict
    ):
        supplement = LEVEL_STEP * traffics[round(employee["last_time"])] + LEVEL_START
        duration = durations[employee["position_id"]][task["point_id"]]
        duration = duration * supplement
        return duration, supplement

    def __check_match_grade(self, task: dict, employee: dict):
        for g in task["grades"]:
            if employee["grade"]["id"] == g["id"]:
                return True
        return False

    def __select_tasks(
        self,
        tasks: list,
        employees: list,
        max_task_dur: int,
        max_prior_val: int,
        grades: dict,
        traffics: dict,
        durations: dict,
        max_dur_go: int,
        end_hour_inp: int,
    ):
        flag = True
        # раздаем по одной по кругу, как при раздаче в картах
        while flag:
            flag = False
            is_change = False
            for e in employees:
                max_match = {"value": 0, "task": None}
                for t in tasks:
                    # задача не занята и грейд сотрудника соответствует задачи
                    if not t["is_select"] and e["grade"] in t["grades"]:
                        # вычисляем время в дороге
                        dur, supplement = self.__calc_duration(
                            t, e, traffics, durations
                        )
                        dur_go_hour = dur / HOUR_IN_SECONDS
                        # во сколько по часам закончит
                        end_hour = e["last_time"] + dur_go_hour + t["duration"]

                        if end_hour <= end_hour_inp:
                            # нормализация
                            t["duration_std"] = self.__standart_value(
                                max_task_dur, t["duration"], False
                            )
                            t["priority_value_std"] = self.__standart_value(
                                max_prior_val, t["priority_value"]
                            )
                            std_dur_go = self.__standart_value(
                                max_dur_go * supplement, dur
                            )

                            # вычисления соответствия задачи
                            new_match_value = self.__calculate_match(
                                e, t, grades, std_dur_go
                            )
                            if max_match["value"] < new_match_value:
                                max_match["value"] = new_match_value
                                max_match["task"] = t
                                max_match["begin_hour"] = e["last_time"]
                                max_match["end_hour"] = end_hour

                if max_match["value"] > 0 and max_match["task"]:
                    max_match["task"]["is_select"] = True
                    e["last_time"] = max_match["end_hour"]
                    e["tasks"].append(max_match)
                    e["position_id"] = self.__gen_key(
                        max_match["task"]["point_id"], False
                    )
                    is_change = True

            if is_change:
                flag = True

    def __standart_value(self, max: int, value: int, is_max: bool = True):
        value = value / max if max > 0 else 0
        if is_max:
            return value
        else:
            return 1 - value

    def __calc_grade_ratios(self, grades: list[Grade]):
        ratios = {}
        for i in grades:
            r = {}
            for j in reversed(grades):
                if i.value >= j.value:
                    r[j.id] = round(j.value / i.value, 2)
            ratios[i.id] = r
        return ratios

    async def __proccess_tasks(self):
        new_tasks = []
        tasks = await self.__uow.tasks.get_all_full()
        association_taks = {}
        max_duration = 0
        max_priority_value = 0
        user_ids = []

        for t in tasks:
            association_taks[t.id] = t
            grades = []
            for g in t.type.grade_links:
                grades.append({"id": g.grade_id, "value": g.grade.value})

            d = t.type.duration
            p = t.priority.value
            if d > max_duration:
                max_duration = d
            if p > max_priority_value:
                max_priority_value = p
            if t.employee_id:
                user_ids.append(t.employee_id)
            new_tasks.append(
                {
                    "is_select": False,
                    "id": t.id,
                    "priority_value": p,
                    "point_id": t.point_id,
                    "duration": d,
                    "skills": {s.skill_id for s in t.type.skill_links},
                    "grades": grades,
                }
            )
        return new_tasks, max_duration, max_priority_value, association_taks, user_ids

    def __gen_key(self, id: int, is_office: bool = True):
        return f"{id}_{'o' if is_office else'p'}"

    async def __proccess_employees(self, user_ids: list[int], begin_hour: int):
        employees = await self.__uow.employees.get_all_full(is_active=True)
        random.shuffle(employees)
        new_employees = []
        for e in employees:
            if e.id in user_ids:
                continue
            employee = {
                "count_t": 0,
                "last_time": begin_hour,
                "id": e.id,
                "email": e.user.email,
                "grade": {"id": e.grade_id, "value": e.grade.value},
                "skills": {sl.skill_id for sl in e.skill_links},
                "tasks": [],
                "position_id": self.__gen_key(e.office_id),
            }
            new_employees.append(employee)
        return new_employees

    def __proccess_durs(
        self,
        items: list,
        durations: dict,
        max_dur: int,
        is_office: bool,
    ):
        for d in items:
            v = d.value
            if v > max_dur:
                max_dur = v
            if is_office:
                key = self.__gen_key(d.office_id, is_office)
                durations.setdefault(key, {})
                durations[key][d.point_id] = v

            else:
                key = self.__gen_key(d.point_id1, is_office)
                durations.setdefault(key, {})
                durations[key][d.point_id2] = v

        return max_dur

    async def distribution_tasks_to_all(self, begin_hour: int, end_hour: int):
        async with self.__uow:
            try:
                (
                    tasks,
                    max_dur,
                    max_prior_val,
                    association_taks,
                    user_ids,
                ) = await self.__proccess_tasks()
                new_employees = await self.__proccess_employees(user_ids, begin_hour)
                grades = await self.__uow.grades.get_all()

                traffics = {
                    t.hour: t.level for t in await self.__uow.traffics.get_all()
                }

                durations = {}
                max_dur_go = 0
                o_durs = await self.__uow.office_durations.get_all()
                p_durs = await self.__uow.point_durations.get_all()
                max_dur_go = self.__proccess_durs(o_durs, durations, max_dur_go, True)
                max_dur_go = self.__proccess_durs(p_durs, durations, max_dur_go, False)

                grades = self.__calc_grade_ratios(grades)
                self.__select_tasks(
                    tasks,
                    new_employees,
                    max_dur,
                    max_prior_val,
                    grades,
                    traffics,
                    durations,
                    max_dur_go,
                    end_hour,
                )
                date_now = datetime.utcnow()
                broadcast_msg = []
                for e in new_employees:
                    broadcast_msg.append(
                        {"id": e["id"], "msg": TASK_DISTRIBUTED, "email": e["email"]}
                    )
                    for t in e["tasks"]:
                        task = association_taks[t["task"]["id"]]
                        task.employee_id = e["id"]
                        task.status_id = EXECUTE_ID
                        task.date_begin = date_now.replace(
                            hour=round(t["begin_hour"]),
                            minute=0,
                            second=0,
                            microsecond=0,
                        )
                        await self.__uow.tasks.add(task)
                await self.__uow.commit()
                return MessageSchema(message=TASKS_DISTRIBUTIONED), broadcast_msg
            except Exception as e:
                raise AnyServiceException(TASKS_DISTRIBUTION_FAILED) from e

    async def _create_task_for_history(
        self,
        task_db: Task,
        status_id: int,
        feedback_val: int | None = None,
        feedback_descp: str | None = None,
    ):
        async with self.__uow:

            def object_as_dict(obj):
                if obj is not None:
                    d = {
                        c.key: getattr(obj, c.key)
                        for c in inspect(obj).mapper.column_attrs
                    }
                    return d
                else:
                    return None

            type_db = await self.__uow.type_tasks.get_by_id(task_db.type_id)
            point_db = await self.__uow.points.get_by_id(task_db.point_id)
            point_ = object_as_dict(point_db)
            del point_["created_at"]
            del point_["last_date_issue_card"]
            employee_db = await self.__uow.employees.get_by_id(task_db.employee_id)
            employee_ = object_as_dict(employee_db)
            if employee_ is not None:
                user_db = await self.__uow.users.get_by_id(employee_["id"])
                user_ = object_as_dict(user_db)
                del user_["created_at"]
                del user_["hashed_password"]
                grade_db = await self.__uow.grades.get_by_id(employee_["grade_id"])
                employee_["id"] = user_
                employee_["grade_id"] = object_as_dict(grade_db)
            history_task_db = HistoryTask(
                type=object_as_dict(type_db),
                type_id=task_db.type_id,
                point=point_,
                point_id=task_db.point_id,
                status_id=status_id,
                employee=employee_,
                employee_id=task_db.employee_id,
                date_begin=task_db.date_begin,
                date_create=task_db.date_create,
                feedback_value=feedback_val,
                feedback_description=feedback_descp,
            )
            return history_task_db

    # def __proccess_formula(self, formula: dict, fields: dict):
    #     new_formula = copy(formula)
    #     for k, v in formula.items():
    #         if k.startswith("$"):
    #             if isinstance(v, dict):
    #                 for key, value in v.items():
    #                     if type(value) is str and value in fields:
    #                         new_value = fields[value]
    #                         new_formula[k][key] = new_value
    #         else:
    #             if type(k) is str and k in fields:
    #                 new_key = fields[k]

    #                 if type(v) is str and v.lower() in LOGIC_BIT:
    #                     v = LOGIC_BIT[v.lower()]
    #                 new_formula[new_key] = v
    #                 del new_formula[k]
    #     return new_formula
