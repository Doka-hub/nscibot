from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

# local imports
from models.bot import objects, TGUser, DoesNotExist


class WhiteListFilter(BoundFilter):
    key = 'in_whitelist'

    def __init__(self, in_whitelist):
        self.in_whitelist = in_whitelist

    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        try:
            user = await objects.get(TGUser.filter(TGUser.user_id == user_id))
            return user.can_use_bot
        except DoesNotExist:
            return False
