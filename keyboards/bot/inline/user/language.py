from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# local imports
from keyboards.bot.utils import get_inline_keyboard


def get_language_inline_keyboard() -> InlineKeyboardMarkup:
    language_inline_keyboard = get_inline_keyboard(
        [
            [InlineKeyboardButton('🇷🇺 русский', callback_data='choose_language ru')],
            [InlineKeyboardButton('🇺🇸 english', callback_data='choose_language en')],
        ]
    )
    return language_inline_keyboard
