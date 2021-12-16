# local imports
from utils.bot.db_api.user import get_or_create_user

from models.bot import objects


async def add_to_whitelist_(user_id: int):
    user, user_created = await get_or_create_user(user_id)
    if not user.can_use_bot:
        user.can_use_bot = True
        await objects.update(user, ['can_use_bot'])


async def remove_from_whitelist_(user_id: int):
    user, user_created = await get_or_create_user(user_id)
    if user.can_use_bot:
        user.can_use_bot = False
        await objects.update(user, ['can_use_bot'])
