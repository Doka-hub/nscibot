# local imports
from models.bot import objects, TGUser

from .user import get_or_create_user


async def get_language(user_id: int) -> TGUser.language:
    user, user_created = await get_or_create_user(user_id)
    return user.language


async def set_language(user_id: int, language: str):
    user, user_created = await get_or_create_user(user_id)
    user.language = language
    await objects.update(user, ['language'])
