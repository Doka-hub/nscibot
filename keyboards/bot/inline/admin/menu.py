from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# local imports
from filters.bot.is_admin import AdminFilter

from keyboards.bot.utils import get_inline_keyboard

from loader import bot_i18n_gettext as _


def get_menu_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    menu_inline_keyboard = get_inline_keyboard(
        [
            [InlineKeyboardButton(_('Написать подписчикам', locale=locale), callback_data='mail')],
        ] if AdminFilter().check_by_user_id(user_id) else
        [

        ]
    )
    return menu_inline_keyboard
