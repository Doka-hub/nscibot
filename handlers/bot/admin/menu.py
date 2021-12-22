from aiogram import types

# local imports
from keyboards.bot.inline.admin.menu import get_menu_inline_keyboard

from loader import bot_i18n_gettext as _


async def menu(callback: types.CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id

    menu_inline_keyboard = get_menu_inline_keyboard(user_id=user_id)
    await callback.message.answer(_('Меню'), reply_markup=menu_inline_keyboard)
