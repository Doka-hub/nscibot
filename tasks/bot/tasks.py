import asyncio

# local imports
from tasks.celery import app

from loader import bot_dp

from .mail import mail


# mail
@app.task(name='provider_bot__mail')
def task_mail(mail_data: dict):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mail(mail_data))
