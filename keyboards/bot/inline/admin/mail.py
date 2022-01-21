from typing import List, Dict, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# local imports
from keyboards.bot.utils import get_inline_keyboard

from utils.bot.db_api.admin.mail import get_message_template_list

from loader import bot_i18n_gettext as _


async def get_group_list_to_mail_inline_keyboard() -> InlineKeyboardMarkup:
    group_list_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(_('Подписчикам'),
                                     callback_data='mail_subscribers'),
                # InlineKeyboardButton(_('Покупателям'),
                #                      callback_data='mail_subscribers')
            ]
        ],
        True, 'menu'
    )
    return group_list_inline_keyboard


def get_mail_create_message(mail_data: Dict) -> str:
    title = mail_data.get('title')
    text = mail_data.get('text')

    message = (
        f'*{title}*\n\n{text}' if title and text else
        f'*{title}*\n\n' if title and not text else
        f'{text}' if text and not title else
        _('Создание рассылки:\n')
    )
    return message


def get_mail_detail_inline_button(button: str) -> Optional[List[InlineKeyboardButton]]:
    """
    Получаем  кнопку для клавиатуры
    :param button:
    :return:
    """
    if not button:
        return
    button_text, button_url = button.split(' - ')
    mail_detail_inline_button = [
        InlineKeyboardButton(button_text, url=button_url)
    ]
    return mail_detail_inline_button


def get_mail_message_buttons_inline_keyboard(
        buttons: List[str]) -> Optional[InlineKeyboardMarkup]:
    """
    Получаем кнопки для рассылки
    :param buttons:
    :return:
    """
    if not buttons:
        return

    mail_message_buttons_inline_keyboard = [
        [
            InlineKeyboardButton(
                button.split(' - ')[0],
                url=button.split(' - ')[1]
            )
        ] for button in buttons if isinstance(button, str)
    ]
    return get_inline_keyboard(mail_message_buttons_inline_keyboard)


def get_mail_create_inline_keyboard(mail_data: Dict) -> InlineKeyboardMarkup:
    mail_detail_inline_button = get_mail_detail_inline_button(mail_data.get('button1')) or []
    mail_detail_inline_button2 = get_mail_detail_inline_button(mail_data.get('button2')) or []
    mail_detail_inline_button3 = get_mail_detail_inline_button(mail_data.get('button3')) or []
    mail_detail_inline_button4 = get_mail_detail_inline_button(mail_data.get('button4')) or []

    mail_create_inline_keyboard = get_inline_keyboard(
        [
            mail_detail_inline_button, mail_detail_inline_button2, mail_detail_inline_button3,
            mail_detail_inline_button4,
            [
                InlineKeyboardButton(
                    _('Добавить изображение или видео') if not mail_data.get('image_id') else
                    _('Изменить изображение или видео'),
                    callback_data='mail_create__image' if not mail_data.get('image_id') else 'mail_update__image'
                ),
            ],
            [
                InlineKeyboardButton(
                    _('Добавить заголовок') if not mail_data.get('title') else _('Изменить заголовок'),
                    callback_data='mail_create__title' if not mail_data.get('title') else 'mail_update__title'
                ),
                InlineKeyboardButton(
                    _('Добавить текст') if not mail_data.get('text') else _('Изменить текст'),
                    callback_data='mail_create__text' if not mail_data.get('text') else 'mail_update__text'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Добавить кнопку 1') if not mail_data.get('button1') else _('Изменить кнопку 1'),
                    callback_data='mail_create__button1' if not mail_data.get('button1') else 'mail_update__button1'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Добавить кнопку 2') if not mail_data.get('button2') else _('Изменить кнопку 2'),
                    callback_data='mail_create__button2' if not mail_data.get('button2') else 'mail_update__button2'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Добавить кнопку 3') if not mail_data.get('button3') else _('Изменить кнопку 3'),
                    callback_data='mail_create__button3' if not mail_data.get('button3') else 'mail_update__button3'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Добавить кнопку 4') if not mail_data.get('button4') else _('Изменить кнопку 4'),
                    callback_data='mail_create__button4' if not mail_data.get('button4') else 'mail_update__button4'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Выбрать время для рассылки') if not mail_data.get('time_to_mail') else
                    _('Изменить время для рассылки'),
                    callback_data='mail_create__time_to_mail'
                ),
                InlineKeyboardButton(
                    _('Разослать'),
                    callback_data='mail_send'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Сохранить шаблон'),
                    callback_data=f'mail_create__template_save'
                ),
                InlineKeyboardButton(
                    _('Выбрать шаблон'),
                    callback_data=f'mail_create__template_list'
                )
            ],
            [
                InlineKeyboardButton(
                    _('Отмена'),
                    callback_data=f'mail_create__cancel'
                )
            ],
        ]
    )
    return mail_create_inline_keyboard


def get_mail_create_data_cancel_inline_keyboard() -> InlineKeyboardMarkup:
    """
    :return: Возвращает inline-клавиатуру с отменой заполнения того или иного поля
    """
    mail_create_data_cancel_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(_('Отмена'), callback_data='mail_create__data_cancel')
            ]
        ]
    )
    return mail_create_data_cancel_inline_keyboard


async def get_message_template_list_inline_keyboard(user_id: int, page: Optional[int] = 1,
                                                    limit: Optional[int] = 10) -> InlineKeyboardMarkup:
    """
    :return: Возвращает inline-клавиатуру со списком mail-шаблонов
    """
    message_template_list_info = await get_message_template_list(user_id, page, limit)

    message_template_list = [
         [
             InlineKeyboardButton(_('Шаблон {}').format(message_template.name),
                                  callback_data=f'mail_create__message_template_choose {message_template.id}'),
             InlineKeyboardButton(_('Удалить'),
                                  callback_data=f'mail_create__message_template_delete {message_template.id}'),
         ] for message_template in message_template_list_info['message_template_list']
    ]

    is_pagination = message_template_list_info['is_pagination']
    if is_pagination:
        current_page = message_template_list_info['current_page']
        page_count = message_template_list_info['page_count']
        next_page = current_page + 1 if not current_page + 1 > page_count else current_page
        prev_page = current_page - 1 if not current_page - 1 <= 0 else current_page
        message_template_list += [[
            InlineKeyboardButton('<', callback_data=f'message_template_prev_page#{prev_page}'),
            InlineKeyboardButton(f'{current_page}/{page_count}', callback_data='mail_template_curr_page'),
            InlineKeyboardButton('>', callback_data=f'message_template_next_page#{next_page}'),
        ]]

    mail_template_list_inline_keyboard = get_inline_keyboard(message_template_list, True,
                                                             'mail_create__message_template_choose_cancel')
    return mail_template_list_inline_keyboard
