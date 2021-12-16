import os

from uuid import uuid4

import pandas as pd

from aiogram import types

# local imports
from keyboards.bot.inline.user import get_menu_inline_keyboard

from utils.bot.db_api.user import get_user_list
from utils.bot import set_commands

from loader import bot_i18n_gettext as _


@set_commands
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    menu_inline_keyboard = get_menu_inline_keyboard(user_id=user_id)
    await message.answer(_('Меню'), reply_markup=menu_inline_keyboard)
