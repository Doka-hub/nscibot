from typing import List, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# local imports
from loader import bot_i18n_gettext as _


def get_inline_keyboard(data: List[List[InlineKeyboardButton]],
                        is_back_button: Optional[bool] = False,
                        back_button_callback_data: Optional[str] = None) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(row_width=6)
    for row in data:
        inline_keyboard.row(*row)

    # добавляем кнопку назад (если нужна)
    if is_back_button:
        inline_keyboard.row(InlineKeyboardButton(_('Назад'), callback_data=back_button_callback_data))
    return inline_keyboard
