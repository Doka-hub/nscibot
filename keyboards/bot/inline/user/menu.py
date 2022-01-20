from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# local imports
from keyboards.bot.utils import get_inline_keyboard

from loader import bot_i18n_gettext as _

from data.config import MODERATOR_USERNAME, HELPER_USERNAME


def get_menu_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    menu_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(_('Баланс', locale=locale), callback_data='balance'),
                InlineKeyboardButton(_('Реферальная программа', locale=locale), callback_data='referral')
            ],
            [
                InlineKeyboardButton(_('Дополнительно', locale=locale), callback_data='more'),
                InlineKeyboardButton(_('Новости', locale=locale), callback_data='news')
            ],
            [
                InlineKeyboardButton(_('Телеграм группа', locale=locale), url='https://t.me/NSCI_Chat'),
                InlineKeyboardButton(_('Канал', locale=locale), url='https://t.me/NSCIVenture')
            ],
            [
                InlineKeyboardButton(_('Сменить язык', locale=locale), callback_data='change_language')
            ]
        ]
    )
    return menu_inline_keyboard


def get_balance_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    balance_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(_('Купить', locale=locale), url=f't.me/{MODERATOR_USERNAME}'),
                InlineKeyboardButton(_('Продать', locale=locale), url=f't.me/{MODERATOR_USERNAME}')
            ],
            [InlineKeyboardButton(_('Вывести на кошелек', locale=locale), callback_data='withdraw')],
        ], True, 'menu'
    )
    return balance_inline_keyboard


def get_referral_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    referral_inline_keyboard = get_inline_keyboard(
        [
            [InlineKeyboardButton(_('Мои рефералы', locale=locale), callback_data='referral_list')],
        ], True, 'menu'
    )
    return referral_inline_keyboard


def get_more_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    more_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(_('Поддержка', locale=locale), url=f't.me/{HELPER_USERNAME}'),
                InlineKeyboardButton(_('Сайт', locale=locale), url='https://nsci.space/')
            ],
            [InlineKeyboardButton(_('Курс', locale=locale), callback_data='get_exchange_rate')],
            # [InlineKeyboardButton(_('Скачать кошелек', locale=locale), callback_data='withdraw')],
        ], True, 'menu'
    )
    return more_inline_keyboard



def get_news_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    news_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(_('Телеграм', locale=locale), url='t.me/NSCIVenture'),
                InlineKeyboardButton(_('Твиттер', locale=locale), url='https://twitter.com/nsci_official')
                ],
        ], True, 'menu'
    )
    return news_inline_keyboard


def get_back_to_menu_inline_keyboard(locale: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    back_to_menu_inline_keyboard = get_inline_keyboard([], True, 'menu')
    return back_to_menu_inline_keyboard
