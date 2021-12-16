from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# local imports
from loader import bot_i18n_gettext as _


def get_request_contact_default_keyboard() -> ReplyKeyboardMarkup:
    get_contact_default_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton(_('Подписаться'), request_contact=True)]
        ], one_time_keyboard=True
    )
    return get_contact_default_keyboard
