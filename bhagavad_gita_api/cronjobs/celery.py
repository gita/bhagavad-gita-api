import requests
from celery import Celery
from celery.schedules import crontab

from bhagavad_gita_api.config import settings

app = Celery(
    "cronjobs",
    broker=settings.REDIS_BROKER,
    backend=settings.REDIS_BACKEND,
)


app.conf.timezone = "UTC"


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        set_verse.s(),
    )


@app.task
def set_verse():
    url = "{}/v2/set-daily-verse".format(settings.CRONJOB_BASE_URL)
    data = {
        "accept": "application/json",
        "X-API-KEY": settings.X_API_KEY,
    }
    r = requests.post(url=url, data=data, headers=data)
    print(r)


if __name__ == "__main__":
    app.start()
