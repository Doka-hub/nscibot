from datetime import datetime

# local imports
from data import config

from keyboards.bot.inline.admin.mail import (
    get_mail_message_buttons_inline_keyboard
)

from models.bot import objects, Order

from utils.bot.db_api.user import (
    get_user_list as get_provider_user_list
)
from utils.bot.db_api.order import (
    get_user_list_to_send_orders as get_provider_user_list_to_send_orders
)
from utils.bot.db_api.user import (
    get_user_list as get_subscriber_user_list
)

from tasks.bot.utils.mailing import (
    send_message as provider_send_message
)
from tasks.subscriber_bot.utils.mailing import (
    send_message as subscriber_send_message
)


async def mail(mail_data: dict):
    group = mail_data.get('group')
    image_id = mail_data.get('image_id')
    video_id = mail_data.get('video_id')
    document = mail_data.get('document')
    title = mail_data.get('title')
    text = mail_data.get('text')
    button = mail_data.get('button1')
    button2 = mail_data.get('button2')
    button3 = mail_data.get('button3')
    button4 = mail_data.get('button4')
    mail_message_buttons_inline_keyboard = \
        get_mail_message_buttons_inline_keyboard(
            [button, button2, button3, button4]
        ) or None

    if group == 'providers':
        user_list = await get_provider_user_list()
        for user in user_list:
            to = user.user_id
            await provider_send_message(
                to, title, text, None, image_id, video_id, document,
                'markdown', mail_message_buttons_inline_keyboard)
    elif group == 'subscribers':
        user_list = await get_subscriber_user_list()
        for user in user_list:
            to = user.user_id
            await subscriber_send_message(
                to, title, text, None, image_id, video_id, None, document,
                'markdown', mail_message_buttons_inline_keyboard)


async def orders_send():
    today = datetime.today().date()
    user_list_to_send_orders = \
        await get_provider_user_list_to_send_orders(today)
    for user_to_send_order in user_list_to_send_orders:
        user_id = user_to_send_order.user_id
        user_phone = user_to_send_order.phone_number
        print(user_id)

        url = user_to_send_order.get_order_url_by_date(today)
        message = f'📦 Новый заказ за {today}'
        buttons_inline_keyboard = get_mail_message_buttons_inline_keyboard(
            [f'➡️Открыть заказ - {url}']
        )

        sent = await provider_send_message(
            user_id, message=message, parse_mode='markdown',
            reply_markup=buttons_inline_keyboard
        )
        if sent:  # если сообщение доставлено
            orders = await objects.execute(
                user_to_send_order.orders.filter(Order.notify == True)
            )
            for order in orders:
                order.notify = False
                await objects.update(order, ['notify'])

            for admin_id in config.PROVIDER_BOT_ADMINS:
                message = f'''📦 Заказ от поставщика {user_phone}
📅 За {today}'''
                await provider_send_message(
                    admin_id, message=message,
                    reply_markup=buttons_inline_keyboard
                )
