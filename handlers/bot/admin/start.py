from aiogram import types

# local imports
from keyboards.bot.inline.admin.menu import get_menu_inline_keyboard

from utils.bot import set_commands

from loader import bot_i18n_gettext as _


@set_commands
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    menu_inline_keyboard = get_menu_inline_keyboard(user_id=user_id)
    await message.answer(_('Меню'), reply_markup=menu_inline_keyboard)
