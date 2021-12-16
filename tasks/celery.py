from celery import Celery
from celery.schedules import timedelta, crontab

# local imports
from data import config

# from .provider_bot import tasks as provider_tasks
# from .subscriber_bot import tasks as subscriber_tasks


app = Celery('app', broker=config.REDIS['ip'])

app.conf.timezone = config.TIMEZONE
app.conf.enable_utc = True
app.conf.beat_schedule = {
   'provider_bot__order_date_move': {
       'task': 'provider_bot__order_date_move',
       'schedule': crontab(hour=5, minute='10')
   },
   'provider_bot__notify': {
       'task': 'provider_bot__notify',
       'schedule': crontab(hour=5, minute='00', day_of_week='mon,sun,fri')
   },
}
