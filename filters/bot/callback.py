from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class CallbackData(BoundFilter):
    key = 'callback_data'

    def __init__(self, callback_data):
        self.callback_data = callback_data

    async def check(self, callback: types.CallbackQuery) -> bool:
        return callback.data == self.callback_data


class CallbackDataStartsWith(BoundFilter):
    key = 'callback_data__startswith'

    def __init__(self, callback_data__startswith):
        self.callback_data = callback_data__startswith

    async def check(self, callback: types.CallbackQuery) -> bool:
        return callback.data.startswith(self.callback_data)
