from copy import copy
from time import sleep
from src.database.exceptions import (
    AddItemException,
    DeleteItemException,
    GetAllItemsException,
    GetItemByIdException,
    UpdateItemException,
)
from src.office.const import BLOCK_FIELD
from src.schemas.message import MessageSchema
from src.schemas.response_items import ResponseItemsSchema
from src.services.unit_of_work import IUnitOfWork
from src.office.schemas import *
from src.office.phrases import *
from src.office.exceptions import *
from src.utils import check_count_items, check_exist_items
from src.exceptions import *
from src.config import settings
import requests
from fastapi import UploadFile
from datetime import date, datetime
import random
import json


class OfficeService:
    def __init__(self, uow: IUnitOfWork):
        self.__uow = uow

    async def get_offices(
        self, limit: int | None, offset: int | None, substr: str | None
    ) -> ResponseItemsSchema[OfficeSchema]:
        async with self.__uow:
            try:
                offices = await self.__uow.offices.get_all_full(
                    limit,
                    offset,
                    substr,
                )
                l = check_count_items(offices, OFFICES_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [OfficeSchema.from_orm(o) for o in offices], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def get_by_id(self, id: int) -> OfficeSchema:
        async with self.__uow:
            try:
                office = await self.__uow.offices.get_by_id(id)
                check_exist_items(office, OFFICE_NOT_FOUND)
                return OfficeSchema.from_orm(office)
            except GetItemByIdException as e:
                raise NotFoundException(OFFICE_NOT_FOUND) from e

    async def post_office(self, office: OfficePostSchema):
        async with self.__uow:
            try:
                url = settings.YANDEX_URL.format(
                    office.address, settings.YANDEX_KEY_API_LOC
                )
                res = requests.get(url)
                if res.status_code == 200:
                    data = res.json()
                    coords = {
                        "y": data["features"][0]["geometry"]["coordinates"][0],
                        "x": data["features"][0]["geometry"]["coordinates"][1],
                    }
                    office_db = Office(address=office.address, coordinate=coords)
                    await self.__uow.offices.add(office_db)
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_ADD_SUCCESS)
            except AddItemException as e:
                raise AnyServiceException(message=OFFICE_ADD_FAILED) from e

    async def put_office(self, office: OfficePutSchema):
        async with self.__uow:
            try:
                office_db = await self.__uow.offices.get_by_id(office.id)
                check_exist_items(office_db, OFFICE_NOT_FOUND)
                if office.coordinate is not None:
                    office_db.coordinate = office.coordinate
                    office_db.address = office.address
                elif office_db.address != office.address:
                    url = settings.YANDEX_URL.format(
                        office.address, settings.YANDEX_KEY_API_LOC
                    )
                    res = requests.get(url)
                    if res.status_code == 200:
                        data = res.json()
                        coords = {
                            "y": data["features"][0]["geometry"]["coordinates"][0],
                            "x": data["features"][0]["geometry"]["coordinates"][1],
                        }
                        office_db.address = office.address
                        office_db.coordinate = coords
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_UPDATE_SUCCESS)
            except GetItemByIdException as e:
                raise NotFoundException(OFFICE_NOT_FOUND) from e
            except UpdateItemException as e:
                raise AnyServiceException(message=OFFICE_UPDATE_FAILED) from e

    async def delete_office(self, id: int):
        async with self.__uow:
            try:
                office_exist = await self.__uow.offices.get_by_id(id)
                check_exist_items(office_exist, OFFICE_NOT_FOUND)
                await self.__uow.offices.delete(id=id)
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OFFICE_DELETE_FAILED) from e

    async def get_points(
        self, limit: int | None, offset: int | None, substr: str | None
    ) -> ResponseItemsSchema[PointSchema]:
        async with self.__uow:
            try:
                points = await self.__uow.points.get_all_full(
                    limit,
                    offset,
                    substr,
                )
                l = check_count_items(points, OFFICES_NOT_FOUND)
                return ResponseItemsSchema.Of(
                    [PointSchema.from_orm(p) for p in points], offset, l
                )
            except GetAllItemsException as e:
                raise NotFoundException(e.message) from e

    async def delete_point(self, id: int):
        async with self.__uow:
            try:
                point_exist = await self.__uow.points.get_by_id(id)
                check_exist_items(point_exist, OFFICE_NOT_FOUND)
                await self.__uow.points.delete(id=id)
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_DELETE_SUCCESS)
            except DeleteItemException as e:
                raise AnyServiceException(message=OFFICE_DELETE_FAILED) from e

    async def post_image_office(self, id: int, file: UploadFile):
        async with self.__uow:
            try:
                files = {"file": (file.filename, file.file, file.content_type)}
                res = requests.post(f"{settings.URL_UPLOAD_FILE}/", files=files)
                r = res.json()
                if res.status_code != 200:
                    raise BadRequestException(r)
                office_db = await self.__uow.offices.get_by_id(id)
                if office_db.img is not None:
                    requests.delete(
                        f"{settings.URL_UPLOAD_FILE}/?filename={office_db.img}"
                    )
                office_db.img = r
                await self.__uow.commit()
                return r
            except Exception as e:
                AnyServiceException()

    async def post_image_point(self, id: int, file: UploadFile):
        async with self.__uow:
            try:
                files = {"file": (file.filename, file.file, file.content_type)}
                res = requests.post(f"{settings.URL_UPLOAD_FILE}/", files=files)
                r = res.json()
                if res.status_code != 200:
                    raise BadRequestException(r)
                point_db = await self.__uow.points.get_by_id(id)
                if point_db.img is not None:
                    requests.delete(
                        f"{settings.URL_UPLOAD_FILE}/?filename={point_db.img}"
                    )
                point_db.img = r
                await self.__uow.commit()
                return r
            except Exception as e:
                AnyServiceException()

    async def post_point(self, point: PointPostSchema):
        async with self.__uow:
            try:
                url = settings.YANDEX_URL.format(
                    point.address, settings.YANDEX_KEY_API_LOC
                )
                res = requests.get(url)
                if res.status_code == 200:
                    data = res.json()
                    coords = {
                        "y": data["features"][0]["geometry"]["coordinates"][0],
                        "x": data["features"][0]["geometry"]["coordinates"][1],
                    }
                    point_db = Point(address=point.address)
                    point_db.coordinate = coords
                    point_db.quantity_card = 0
                    point_db.quantity_requests = 0
                    await self.__uow.points.add(point_db)
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_ADD_SUCCESS)
            except AddItemException as e:
                raise AnyServiceException(message=OFFICE_ADD_FAILED) from e

    async def put_point(self, point: PointPutSchema):
        async with self.__uow:
            try:
                point_db = await self.__uow.points.get_by_id(point.id)
                check_exist_items(point_db, OFFICE_NOT_FOUND)
                if point.coordinate is not None:
                    point_db.coordinate = point.coordinate
                    point_db.address = point.address
                elif point_db.address != point.address:
                    url = settings.YANDEX_URL.format(
                        point.address, settings.YANDEX_KEY_API_LOC
                    )
                    res = requests.get(url)
                    if res.status_code == 200:
                        data = res.json()
                        coords = {
                            "y": data["features"][0]["geometry"]["coordinates"][0],
                            "x": data["features"][0]["geometry"]["coordinates"][1],
                        }
                        point_db.address = point.address
                        point_db.coordinate = coords
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_UPDATE_SUCCESS)
            except GetItemByIdException as e:
                raise NotFoundException(OFFICE_NOT_FOUND) from e
            except UpdateItemException as e:
                raise AnyServiceException(message=OFFICE_UPDATE_FAILED) from e

    async def put_point_is_delivered_card(self, id: int):
        async with self.__uow:
            try:
                point_db = await self.__uow.points.get_by_id(id)
                check_exist_items(point_db, OFFICE_NOT_FOUND)
                point_db.is_delivered_card = True
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_UPDATE_SUCCESS)
            except GetItemByIdException as e:
                raise NotFoundException(OFFICE_NOT_FOUND) from e
            except UpdateItemException as e:
                raise AnyServiceException(message=OFFICE_UPDATE_FAILED) from e

    async def put_quantity_requests(self, id: int, number: int):
        async with self.__uow:
            try:
                point_db = await self.__uow.points.get_by_id(id)
                check_exist_items(point_db, OFFICE_NOT_FOUND)
                point_db.quantity_requests += number
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_UPDATE_SUCCESS)
            except GetItemByIdException as e:
                raise NotFoundException(OFFICE_NOT_FOUND) from e
            except UpdateItemException as e:
                raise AnyServiceException(message=OFFICE_UPDATE_FAILED) from e

    async def put_quantity_card(self, id: int, number: int):
        async with self.__uow:
            try:
                point_db = await self.__uow.points.get_by_id(id)
                check_exist_items(point_db, OFFICE_NOT_FOUND)

                point_db.quantity_card += number
                if point_db.quantity_card >= point_db.quantity_requests:
                    point_db.quantity_card = point_db.quantity_requests
                    point_db.is_delivered_card = False

                point_db.last_date_issue_card = datetime.now()
                await self.__uow.commit()
                return MessageSchema(message=OFFICE_UPDATE_SUCCESS)
            except GetItemByIdException as e:
                raise NotFoundException(OFFICE_NOT_FOUND) from e
            except UpdateItemException as e:
                raise AnyServiceException(message=OFFICE_UPDATE_FAILED) from e

    async def get_dict_point(self):
        res = Point.__dict__
        new_res = []
        for k, v in res.items():
            if not k.startswith("_") and k not in BLOCK_FIELD:
                try:
                    new_res.append(DictPointSchema(ru=v.comment, en=k))
                except:
                    ...
        return new_res

    async def count_weights(self, count_remains: bool):
        async with self.__uow:
            if count_remains == False:
                points = await self.__uow.points.get_all()
                offices = await self.__uow.offices.get_all()
                await self.__uow.point_durations.delete_all()
                await self.__uow.office_durations.delete_all()
                await self.__uow.traffics.delete_all()
                await self.__uow.commit()
                offices_json = await self._calculate_weights_from_office(
                    offices, points
                )
                for i in offices_json:
                    office_dur_db = OfficeDuration(
                        point_id=i["p"],
                        office_id=i["o"],
                        value=i["w"],
                    )
                    await self.__uow.office_durations.add(office_dur_db)
                await self.__uow.commit()
                points_json = await self._calculate_weights_between_points(points, None)
                for i in points_json:
                    point_dur_db = PointDuration(
                        point_id1=i["p1"], point_id2=i["p2"], value=i["w"]
                    )
                    await self.__uow.point_durations.add(point_dur_db)
                await self.__uow.commit()
                traffics_json = await self._calculate_traffic()
                for i in traffics_json:
                    for k, v in i.items():
                        traffic_db = Traffic(hour=int(k), level=v)
                        await self.__uow.traffics.add(traffic_db)
                await self.__uow.commit()


            if count_remains == True:


                points = await self.__uow.points.get_all()
                p_set = set()
                for p in points:
                    p_set.add(p.id)

                offices = await self.__uow.offices.get_all()
                o_set = set()
                for o in offices:
                    o_set.add(o.id)

                office_dur = await self.__uow.office_durations.get_all()
                p_set_dur = set()
                o_set_dur = set()
                for o_d in office_dur:
                    p_set_dur.add(o_d.point_id)
                    o_set_dur.add(o_d.office_id)

                p_ids_not_include = p_set - p_set_dur
                o_ids_not_include = o_set - o_set_dur

                points_db = []
                offices_db = []
                for id in p_ids_not_include:
                    p_db = await self.__uow.points.get_by_id(id)
                    points_db.append(p_db)
                for id in o_ids_not_include:
                    o_db = await self.__uow.offices.get_by_id(id)
                    offices_db.append(o_db)

                offices_json = await self._calculate_weights_from_office(
                    offices_db, points
                )
                for i in offices_json:
                    office_dur_db = OfficeDuration(
                        point_id=i["p"],
                        office_id=i["o"],
                        value=i["w"],
                    )
                    await self.__uow.office_durations.add(office_dur_db)
                offices_json = await self._calculate_weights_from_office(
                    offices, points_db
                )
                for i in offices_json:
                    office_dur_db = OfficeDuration(
                        point_id=i["p"],
                        office_id=i["o"],
                        value=i["w"],
                    )
                    await self.__uow.office_durations.add(office_dur_db)
                await self.__uow.commit()

                points_json = await self._calculate_weights_between_points(points, points_db)
                for i in points_json:
                    point_dur_db = PointDuration(
                        point_id1=i["p1"], point_id2=i["p2"], value=i["w"]
                    )
                    await self.__uow.point_durations.add(point_dur_db)
                await self.__uow.commit()

            return MessageSchema(message=METHOD_WEIGHT_SUCCESS)

    async def _calculate_traffic(self):
        date_today = date.today()
        week_number_now = date_today.weekday()
        step_week = 86400
        step = 3600
        time_start_day = 21600
        timezone = 9
        time_now = (week_number_now + 1) * step_week + time_start_day
        result = []
        for _ in range(9, 19):
            res_url = settings.YANDEX_TRAFFIC_URL.format(time_now)
            res = requests.get(res_url).text
            r = res[res.find("(") + 1 :]
            r = r[:-2]
            js = json.loads(r)
            result.append(
                {
                    timezone: js["data"]["features"][0]["properties"]["JamsMetaData"][
                        "level"
                    ]
                }
            )
            timezone += 1
            time_now += step
            sleep(1)
        return result

    async def _calculate_weights_from_office(self, offices, points):
        res = []
        for o in offices:
            for p in points:
                weight = await self._calculate_weight_between_object(o, p)
                res.append({"o": o.id, "p": p.id, "w": weight})
        return res

    async def _calculate_weights_between_points(self, points, points_not_included):
        res = []
        if points_not_included is None:
            for x in range(len(points) - 1):
                for y in range(x + 1, len(points)):
                    weight1 = await self._calculate_weight_between_object(
                        points[x], points[y]
                    )
                    weight2 = await self._calculate_weight_between_object(
                        points[y], points[x]
                    )
                    res.append({"p1": points[x].id, "p2": points[y].id, "w": weight1})
                    res.append({"p1": points[y].id, "p2": points[x].id, "w": weight2})
        if points_not_included is not None:
            for x in range(len(points_not_included)):
                for y in range(len(points)):
                    if points_not_included[x].id != points[y].id:
                        weight1 = await self._calculate_weight_between_object(
                            points_not_included[x], points[y]
                        )
                        weight2 = await self._calculate_weight_between_object(
                            points[y], points_not_included[x]
                        )
                        res.append({"p1": points_not_included[x].id, "p2": points[y].id, "w": weight1})
                        res.append({"p1": points[y].id, "p2": points_not_included[x].id, "w": weight2})
        return res

    async def _calculate_weight_between_object(self, o1, o2) -> float:
        async with self.__uow:
            # высчитывается нужная таймзона (часы с начала дня), потом обращаться к бд за этим timezone
            # и зависимо от лвла * duration 1lvl - 1,3, 2lvl - 1,4 3lvl - 1,5, 4lvl - 1,6
            # res = duration*(lvl_step*lvl_now+lvl_start)
            # lvl_start = 1
            # lvl_step = 0, 2
            x1 = o1.coordinate["x"]
            y1 = o1.coordinate["y"]
            x2 = o2.coordinate["x"]
            y2 = o2.coordinate["y"]
            res_url = settings.OSRM_API.format(x1, y1, x2, y2)
            res = requests.get(res_url)
            r = res.json()
            if res.status_code != 200:
                raise BadRequestException(r)
            return r["routes"][0]["duration"] + random.randint(60, 300)
