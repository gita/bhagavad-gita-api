import datetime

import pytz
import requests
from celery import Celery
from celery.schedules import crontab

from bhagavad_gita_api.config import settings

app = Celery(
    "cronjobs",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
)
app.conf.timezone = "Asia/Calcutta"


@app.task
def set_verse():
    url = "{}/v2/set-daily-verse/".format(settings.CRONJOB_BASE_URL)
    data = {
        "accept": "application/json",
        "X-API-KEY": settings.TESTER_API_KEY,
    }
    r = requests.post(url=url, data=data, headers=data)
    print(r)


app.conf.beat_schedule = {
    "setup-verse-everyday": {
        "task": "bhagavad_gita_api.cronjobs.celery.set_verse",
        "schedule": crontab(hour=0, minute=0),
    },
}


if __name__ == "__main__":
    app.start()
