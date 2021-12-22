from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

# local imports
from .start import bot_start
from .menu import (
    menu, balance, withdraw,
     referral, referral_list,
     more, news,
     get_exchange_rate
)
from .language import choose_language, change_language


def setup(dp: Dispatcher):
    # Старт
    dp.register_message_handler(bot_start, CommandStart())

    # # Обработка контакта
    # dp.register_message_handler(contact__handler, content_types=types.ContentType.CONTACT)

    # Меню
    dp.register_callback_query_handler(menu, callback_data='menu')
    dp.register_callback_query_handler(balance, callback_data='balance')
    dp.register_callback_query_handler(referral, callback_data='referral')
    dp.register_callback_query_handler(referral_list, callback_data='referral_list')
    dp.register_callback_query_handler(more, callback_data='more')
    dp.register_callback_query_handler(news, callback_data='news')
    dp.register_callback_query_handler(withdraw, callback_data='withdraw')
    dp.register_callback_query_handler(get_exchange_rate, callback_data='get_exchange_rate')

    # Язык
    dp.register_callback_query_handler(change_language, callback_data='change_language')
    dp.register_callback_query_handler(choose_language, callback_data__startswith='choose_language ')
