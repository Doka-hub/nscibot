from typing import Union

import asyncio

# local imports
from tasks.celery import app

from loader import provider_dp

from .mail import mail, orders_send
from .order import order_date_move


# mail
@app.task(name='provider_bot__mail')
def task_mail(mail_data: dict):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mail(mail_data))


# notify
@app.task(name='provider_bot__notify')
def task_notify():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(orders_send())


# order date move
@app.task(name='provider_bot__order_date_move')
def task_order_date_move():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(order_date_move())

