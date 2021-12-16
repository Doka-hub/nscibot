from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

# local imports
from .start import bot_start
from .menu import menu
from .whitelist import add_to_whitelist, remove_from_whitelist


def setup(dp: Dispatcher):
    # Старт
    # dp.register_message_handler(bot_start, CommandStart(), is_admin=True)
    # Меню
    dp.register_callback_query_handler(menu, callback_data='menu', is_admin=True)

    dp.register_message_handler(add_to_whitelist, commands='add', is_admin=True)
    dp.register_message_handler(remove_from_whitelist, commands='remove', is_admin=True)
