from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

# local imports
from data import config

from middlewares.bot import i18n


bot = Bot(
    config.BOT_TOKEN, parse_mode=ParseMode.HTML,
    validate_token=True)
bot_storage = MemoryStorage()
bot_dp = Dispatcher(bot, storage=bot_storage)
bot_i18n_gettext = i18n.gettext
