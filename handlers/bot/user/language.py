from aiogram import types

# local imports
from utils.bot.db_api.user import set_language

from keyboards.bot.inline.user import get_menu_inline_keyboard
from keyboards.bot.inline.user.language import get_language_inline_keyboard


from loader import bot_i18n_gettext as _


# Смена языка
async def change_language(callback: types.CallbackQuery) -> None:
    await callback.message.delete()

    language_inline_keyboard = get_language_inline_keyboard()
    await callback.message.answer('Выберите язык / Choose language', reply_markup=language_inline_keyboard)


# Выбор языка
async def choose_language(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    user_language = callback.data[-2:]  # последние два символа это язык ('choose_language ru')
    await set_language(user_id, user_language)

    await callback.message.delete()

    menu_inline_keyboard = get_menu_inline_keyboard(user_id=user_id)
    await callback.message.answer(_('Меню', locale=user_language), reply_markup=menu_inline_keyboard)
