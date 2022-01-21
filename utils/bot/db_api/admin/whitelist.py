# local imports
from utils.bot.db_api.user import get_or_create_user

from models.bot import objects


async def add_to_whitelist_(user_id: int):
    user, user_created = await get_or_create_user(user_id)
    if not user.is_active:
        user.is_active = True
        await objects.update(user, ['is_active'])


async def remove_from_whitelist_(user_id: int):
    user, user_created = await get_or_create_user(user_id)
    if user.is_active:
        user.is_active = False
        await objects.update(user, ['is_active'])
