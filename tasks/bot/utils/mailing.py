from typing import Union, Optional

from asyncio import sleep

from aiogram.types import InlineKeyboardMarkup, InputFile
from aiogram.utils.exceptions import RetryAfter, Unauthorized, BadRequest, \
    BotBlocked

from loguru import logger

# local imports
from utils.bot.db_api.user import get_or_create_user

from models.bot import objects

from loader import bot


def make_text(title: str, text: str) -> str:
    return f'*{title or ""}*' + '\n\n' + f'{text or ""}'


async def send_message(to: Union[str, int], title: Optional[str] = None,
                       text: Optional[str] = None,
                       message: Optional[str] = None,
                       image_id: Optional[str] = None,
                       video_id: Optional[str] = None,
                       document: InputFile = None,
                       parse_mode: Optional[str] = 'markdown',
                       reply_markup: Optional[InlineKeyboardMarkup] = None,
                       disable_notification: Optional[bool] = True,
                       tries: int = 0, max_tries: int = 5) -> bool:
    """
    :param to:
    :param title:
    :param text:
    :param message:
    :param image_id:
    :param video_id:
    :param document:
    :param parse_mode:
    :param reply_markup:
    :param disable_notification: отключаем звук
    :param tries: `n` совершенных проб
    :param max_tries: пробуем отправить сообщение максимум `n` раз
    :return:
    """
    if tries == max_tries - 2:
        await sleep(60)
    elif tries == max_tries - 1:
        await sleep(60)
    elif tries >= max_tries:
        return False
    logger.info('send to: {to}', to=to)
    try:
        if not message:
            message = make_text(title, text)
        if image_id:
            await bot.send_photo(
                to, image_id, message, parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_notification=disable_notification)
        elif video_id:
            await bot.send_video(
                to, video_id, caption=message, parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_notification=disable_notification)
        elif document:
            await bot.send_document(
                to, document, reply_markup=reply_markup,
                disable_notification=disable_notification)
        else:
            await bot.send_message(
                to, message, parse_mode=parse_mode, reply_markup=reply_markup,
                disable_notification=disable_notification)
        return True
    except RetryAfter as e:
        # error = f'{e}'
        # time = error[error.find('Retry in ') + len('Retry in '):error.find(
        #     ' seconds')]  # сколько нужно ждать
        await sleep(float(e.timeout) + 2)
        return await send_message(to, title, text, message, image_id, video_id,
                                  document, parse_mode, reply_markup,
                                  disable_notification, tries + 1, max_tries)
    except BotBlocked as e:
        if not f'{to}'.startswith('-'):
            user, user_created = await get_or_create_user(to)
            user.bot_blocked_by_user = True
            await objects.update(user, ['bot_blocked_by_user'])
    except Unauthorized as e:
        logger.info('Unauthorized: {e}', e=e)
    except BadRequest as e:
        logger.info('BadRequest: {e}', e=e)
    return False
