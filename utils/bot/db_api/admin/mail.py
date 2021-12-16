from typing import Union, Optional, List, Dict

# local imports
from utils.bot.db_api.user import get_or_create_user

from models.bot import objects, MessageTemplate, DoesNotExist


async def get_message_template(message_template_id: int = None,
                               message_template_name: str = None) -> Optional[MessageTemplate]:
    try:
        if message_template_name:
            try:
                return await objects.get(MessageTemplate, name=message_template_name)
            except DoesNotExist:
                return None
        message_template = await objects.get(MessageTemplate, id=message_template_id)
    except DoesNotExist:
        return
    return message_template


async def get_message_template_list(
        user_id: int, page: Optional[int] = None, limit: int = None
) -> Dict[str, Union[List[MessageTemplate], bool, int]]:
    user, user_created = await get_or_create_user(user_id)

    message_template_list = await objects.execute(MessageTemplate.select().where(MessageTemplate.user == user))
    if limit and page is not None:
        page_count = int((len(message_template_list) / limit) + 0.99)  # кол-во страниц
        is_pagination = bool(message_template_list[limit:])  # есть ли следующая страница
        if 0 >= page:
            current_page = 1
        elif page > page_count:
            current_page = page_count
        else:
            current_page = page
        return {'message_template_list': message_template_list[current_page * limit - limit:current_page * limit],
                'is_pagination': is_pagination, 'current_page': current_page, 'page_count': page_count}
    return {'message_template_list': message_template_list}


async def save_message_template(user_id: int, message_template_name: str, mail_data: dict):
    user, user_created = await get_or_create_user(user_id)
    del(mail_data['group'])
    if await get_message_template(message_template_name=message_template_name):
        return 'exist'
    await objects.create(MessageTemplate, user=user, name=message_template_name, data=mail_data)


async def delete_message_template(message_template_id: int):
    channel = await get_message_template(message_template_id=message_template_id)
    await objects.delete(channel)
