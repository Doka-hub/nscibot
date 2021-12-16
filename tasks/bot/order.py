from typing import Union

from datetime import timedelta

# local imports
from models.bot import objects

from utils.bot.db_api.order import get_order_list_to_notify


async def order_date_move():
    order_list = await get_order_list_to_notify()
    for order in order_list:
        order.date += timedelta(days=1)
        await objects.update(order, ['date'])
