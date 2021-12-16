from aiogram import Dispatcher

# local imports
from . import bot


def setup(dp: Dispatcher):
    bot.setup(dp)
