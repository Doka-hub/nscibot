from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

# local imports
from data import config

from filters.bot.callback import CallbackData


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin=True):
        self.is_admin = is_admin

    async def check(self, message: types.Message) -> bool:
        return self.check_by_user_id(message.from_user.id)

    @staticmethod
    def check_by_user_id(user_id: int) -> bool:
        return user_id in config.ADMINS


class BaseAdmin:
    @staticmethod
    async def is_admin(user_id: int):
        return AdminFilter().check_by_user_id(user_id)


class AdminCallbackDataFilter(CallbackData, BaseAdmin):
    key = 'admin_callback_data'

    def __init__(self, admin_callback_data):
        super().__init__(admin_callback_data)

    async def check(self, callback: types.CallbackQuery):
        if not await self.is_admin(callback.from_user.id):
            return False
        return await super().check(callback)
