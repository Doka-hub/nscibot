from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

# local imports
from .start import bot_start
from .menu import menu
from .whitelist import add_to_whitelist, remove_from_whitelist
from .mail import (
    # Выбор группы для рассылки
    mail_group_list_choose,

    # States
    MailState,

    # Создание письма
    mail_create__material_format, mail_create__users, mail_create__cancel,
    mail_create__image, mail_create__title, mail_create__text, mail_create__button, mail_create__time_to_mail,

    # Шаблоны сообщения - CRUD
    mail_create__message_template_list,
    mail_create__message_template_save,
    mail_create__message_template_delete,
    mail_create__message_template_choose, mail_create__message_template_choose_cancel,
    message_template_pagination,

    # Шаблоны сообщения - обработчик
    mail_create__message_template_save__name_handler,

    # Обработчик данных
    mail_create__data_cancel,
    mail_create__image_handler, mail_create__title_handler, mail_create__text_handler, mail_create__button_handler,
    mail_create__time_to_mail_handler,


    # Отправка сообщения
    mail_send,
)


def setup(dp: Dispatcher):
    # Старт
    dp.register_message_handler(bot_start, CommandStart(), is_admin=True)

    # Меню
    dp.register_callback_query_handler(menu, callback_data='menu', is_admin=True)

    dp.register_message_handler(add_to_whitelist, commands='add', is_admin=True)
    dp.register_message_handler(remove_from_whitelist, commands='remove', is_admin=True)

    # Рассылка
    dp.register_callback_query_handler(mail_group_list_choose,
                                       callback_data='mail')

    # Рассылка - создание
    dp.register_callback_query_handler(
        mail_create__users, callback_data__startswith='mail_subscribers')
    dp.register_callback_query_handler(mail_create__material_format,
                                       callback_data__startswith='mail_create ')

    # Создание рассылки - картинка
    dp.register_callback_query_handler(mail_create__image,
                                       callback_data='mail_create__image')
    dp.register_callback_query_handler(mail_create__image,
                                       callback_data='mail_update__image')
    dp.register_message_handler(mail_create__image_handler,
                                state=MailState.image_id,
                                content_types=types.ContentTypes.ANY)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.image_id)

    # Создание рассылки - заголовок
    dp.register_callback_query_handler(mail_create__title,
                                       callback_data='mail_create__title')
    dp.register_callback_query_handler(mail_create__title,
                                       callback_data='mail_update__title')
    dp.register_message_handler(mail_create__title_handler,
                                state=MailState.title,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.title)

    # Создание рассылки - текст
    dp.register_callback_query_handler(mail_create__text,
                                       callback_data='mail_create__text')
    dp.register_callback_query_handler(mail_create__text,
                                       callback_data='mail_update__text')
    dp.register_message_handler(mail_create__text_handler,
                                state=MailState.text,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.text)

    # Создание рассылки - кнопка
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_create__button1')
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_update__button1')
    dp.register_message_handler(mail_create__button_handler,
                                state=MailState.button1,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.button1)

    # Создание рассылки - кнопка 2
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_create__button2')
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_update__button2')
    dp.register_message_handler(mail_create__button_handler,
                                state=MailState.button2,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.button2)

    # Создание рассылки - кнопка 3
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_create__button3')
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_update__button3')
    dp.register_message_handler(mail_create__button_handler,
                                state=MailState.button3,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.button3)

    # Создание рассылки - кнопка 4
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_create__button4')
    dp.register_callback_query_handler(mail_create__button,
                                       callback_data='mail_update__button4')
    dp.register_message_handler(mail_create__button_handler,
                                state=MailState.button4,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.button4)

    # Рассылка - шаблон
    dp.register_callback_query_handler(mail_create__message_template_save,
                                       callback_data='mail_create__template_save')
    dp.register_message_handler(
        mail_create__message_template_save__name_handler,
        state=MailState.message_template__name,
        content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.message_template__name)
    dp.register_callback_query_handler(mail_create__message_template_list,
                                       callback_data='mail_create__template_list')
    dp.register_callback_query_handler(mail_create__message_template_choose,
                                       callback_data__startswith='mail_create__message_template_choose ')
    dp.register_callback_query_handler(mail_create__message_template_delete,
                                       callback_data__startswith='mail_create__message_template_delete ')
    dp.register_callback_query_handler(
        mail_create__message_template_choose_cancel,
        callback_data='mail_create__message_template_choose_cancel')
    dp.register_callback_query_handler(message_template_pagination,
                                       callback_data__startswith=
                                       'message_template_next_page#' or 'message_template_prev_page#')

    # Рассылка - выбор времени для рассылки
    dp.register_callback_query_handler(mail_create__time_to_mail,
                                       callback_data='mail_create__time_to_mail')
    dp.register_message_handler(mail_create__time_to_mail_handler,
                                state=MailState.time_to_mail,
                                content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(mail_create__data_cancel,
                                       callback_data='mail_create__data_cancel',
                                       state=MailState.time_to_mail)

    # Рассылка - отправка сообщения
    dp.register_callback_query_handler(mail_send, callback_data='mail_send')

    # Рассылка - отмена заполнения
    dp.register_callback_query_handler(mail_create__cancel,
                                       callback_data='mail_create__cancel')
