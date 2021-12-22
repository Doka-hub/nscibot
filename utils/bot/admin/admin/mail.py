from aiogram import types

from typing import Dict, Union, List, Optional

# local imports
from keyboards.bot.inline.admin.mail import get_mail_create_inline_keyboard, get_mail_create_message

from loader import bot_dp


async def mail_create_send_message_detail(*, callback: Optional[types.CallbackQuery] = None,
                                          message: Optional[types.Message] = None):
    """
    Функция отправляет форму для создания поста, подтягивая всю заполненную информацию.

    :param callback: types.CallbackQuery
    :param message: types.Message
    :return: None
    """
    if callback:
        user_id = callback.from_user.id

        mail_data = await bot_dp.storage.get_data(user=user_id)
        from_template = mail_data.get('from_template')
        image_id = mail_data.get('image_id')
        video_id = mail_data.get('video_id')

        mail_create_inline_keyboard = get_mail_create_inline_keyboard(mail_data)
        text_answer = get_mail_create_message(mail_data)

        if image_id:
            if from_template:
                await callback.message.answer_photo(image_id, text_answer, reply_markup=mail_create_inline_keyboard,
                                                    parse_mode='markdown')
            else:
                await callback.message.edit_caption(text_answer, reply_markup=mail_create_inline_keyboard,
                                                    parse_mode='markdown')
        elif video_id:
            if from_template:
                await callback.message.answer_video(video_id, caption=text_answer,
                                                    reply_markup=mail_create_inline_keyboard,
                                                    parse_mode='markdown')
            else:
                await callback.message.edit_caption(text_answer,
                                                    reply_markup=mail_create_inline_keyboard, parse_mode='markdown')
        else:
            if from_template:
                await callback.message.answer(text_answer, reply_markup=mail_create_inline_keyboard,
                                              parse_mode='markdown')
            else:
                await callback.message.edit_text(text_answer, reply_markup=mail_create_inline_keyboard,
                                                 parse_mode='markdown')
    elif message:
        user_id = message.from_user.id

        mail_data = await bot_dp.storage.get_data(user=user_id)
        image_id = mail_data.get('image_id')
        video_id = mail_data.get('video_id')

        mail_create_inline_keyboard = get_mail_create_inline_keyboard(mail_data)
        text_answer = get_mail_create_message(mail_data)

        if image_id:
            await message.answer_photo(image_id, text_answer, reply_markup=mail_create_inline_keyboard,
                                       parse_mode='markdown')
        elif video_id:
            await message.answer_video(video_id, caption=text_answer,
                                       reply_markup=mail_create_inline_keyboard, parse_mode='markdown')
        else:
            await message.answer(text_answer, reply_markup=mail_create_inline_keyboard, parse_mode='markdown')


def check_mail_must_fields_filled(mail_data: Dict) -> List[Union[bool, str]]:
    """
    :param mail_data:
    :return: возвращает список из двух значений. Первое - заполнены ли обязательные поля, второе какие поля не заполнены
    """
    if 'image_id' in mail_data:
        return [True, None]
    elif 'text' in mail_data:
        return [True, None]
    return [False, 'image_or_text']
