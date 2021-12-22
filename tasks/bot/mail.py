# local imports
from keyboards.bot.inline.admin.mail import (
    get_mail_message_buttons_inline_keyboard
)

from utils.bot.db_api.user import (
    get_user_list as get_subscriber_user_list
)

from tasks.bot.utils.mailing import (
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

    if group == 'subscribers':
        user_list = await get_subscriber_user_list()
        for user in user_list:
            to = user.user_id
            await subscriber_send_message(
                to, title, text, None, image_id, video_id, document,
                'markdown', mail_message_buttons_inline_keyboard)

