import requests
from celery.schedules import crontab
import random

from src.config import CeleryConnection, settings
from src.task.const import END_TIME_WORK

MINUTES_IN_SECONDS = 60
TIME_INTERVAL_DEFINE_TASKS = MINUTES_IN_SECONDS * 8
TIME_INTERVAL_CHANGE_POINTS = MINUTES_IN_SECONDS * 30
MAX_CNT_CHANGE_POINT = 10


@CeleryConnection.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=2, minute=0), do_count_weights.s(), name="count_weights"
    )
    sender.add_periodic_task(
        TIME_INTERVAL_DEFINE_TASKS, do_define_tasks.s(), name="define_tasks"
    )
    sender.add_periodic_task(
        TIME_INTERVAL_CHANGE_POINTS,
        do_change_state_points.s(),
        name="change_state_points",
    )
    sender.add_periodic_task(
        crontab(hour=END_TIME_WORK - 3, minute=0),
        do_change_priorities.s(),
        name="change_priority",
    )


@CeleryConnection.task()
def do_count_weights():
    requests.get(f"{settings.URL_ME}/offices/count_weights")


@CeleryConnection.task()
def do_define_tasks():
    requests.post(f"{settings.URL_ME}/tasks/define")


@CeleryConnection.task()
def do_change_priorities():
    requests.put(f"{settings.URL_ME}/tasks/change_priority")


@CeleryConnection.task()
def do_change_state_points():
    all_points = []
    offset = 0
    while True:
        r = requests.get(f"{settings.URL_ME}/offices/points/?offset={offset}")
        offset += 1
        if r.status_code == 404:
            break
        if r.status_code == 200:
            all_points.extend(r.json()["items"])
    cnt = len(all_points)
    count = random.randint(
        1, cnt if cnt <= MAX_CNT_CHANGE_POINT else MAX_CNT_CHANGE_POINT
    )
    c_2 = int(count / 2)

    for i in range(count):
        p = random.choice(all_points)
        num = random.randint(1, 5)
        substr = f"?id={p['id']}&number={num}"
        if i <= c_2:
            requests.put(f"{settings.URL_ME}/offices/points/quantity_requests{substr}")
        else:
            requests.put(f"{settings.URL_ME}/offices/points/quantity_card{substr}")
