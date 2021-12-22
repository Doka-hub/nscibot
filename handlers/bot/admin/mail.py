from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from datetime import timedelta

from celery.schedules import datetime

# local imports
from keyboards.bot.inline.admin.mail import (

    get_mail_create_data_cancel_inline_keyboard,
    get_group_list_to_mail_inline_keyboard,

    # MessageTemplate
    get_message_template_list_inline_keyboard
)

from states.bot.admin import MailState

from utils.bot.admin.admin.mail import mail_create_send_message_detail
from utils.bot.db_api.admin.mail import (
    get_message_template, save_message_template, delete_message_template
)

from tasks.bot.tasks import task_mail
from tasks.bot.mail import mail

from loader import bot_dp, bot_i18n_gettext as _

from .menu import menu


async def mail_group_list_choose(callback: types.CallbackQuery):
    material_format_list_inline_keyboard = await get_group_list_to_mail_inline_keyboard()
    await callback.message.edit_text(
        _('Выберите группу для рассылки'),
        reply_markup=material_format_list_inline_keyboard
    )


async def mail_create__users(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    group = callback.data.replace('mail_', '')

    await bot_dp.storage.set_data(user=user_id, data={'group': group})
    await mail_create_send_message_detail(callback=callback)


async def mail_create__material_format(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    group = callback.data.replace('mail_create ', '')

    await bot_dp.storage.set_data(user=user_id, data={'group': group})
    await mail_create_send_message_detail(callback=callback)


async def mail_create__message_template_save(callback: types.CallbackQuery):
    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()
    if callback.message.content_type in ['photo', 'video']:
        await callback.message.edit_caption(_('Введите название шаблона'),
                                            reply_markup=mail_create_data_cancel_inline_keyboard)
    else:
        await callback.message.edit_text(_('Введите название шаблона'),
                                         reply_markup=mail_create_data_cancel_inline_keyboard)
    await MailState.message_template__name.set()


async def mail_create__message_template_save__name_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    message_template__name = message.text

    if await save_message_template(user_id, message_template__name, data) == 'exist':
        await message.answer(_('Шаблон с таким названием уже существует'))
        return
    await message.answer(_('Шаблон сохранён'))
    await state.reset_state(False)
    await mail_create_send_message_detail(message=message)


async def mail_create__message_template_list(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    template_list_inline_keyboard = await get_message_template_list_inline_keyboard(user_id)
    if callback.message.content_type in ['photo', 'video']:
        await callback.message.edit_caption(_('Выберите шаблон'), reply_markup=template_list_inline_keyboard)
    else:
        await callback.message.edit_text(_('Выберите шаблон'), reply_markup=template_list_inline_keyboard)


async def mail_create__message_template_delete(callback: types.CallbackQuery):
    message_template_id = callback.data.replace('mail_create__message_template_delete ', '')

    await delete_message_template(message_template_id)
    await callback.answer(_('Шаблон удалён'))

    await mail_create__message_template_list(callback)


async def mail_create__message_template_choose(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_template_id = callback.data.replace('mail_create__message_template_choose ', '')

    message_template = await get_message_template(message_template_id)

    await bot_dp.storage.update_data(user=user_id, data={**message_template.data, 'from_template': True})
    await mail_create_send_message_detail(callback=callback)
    await callback.message.delete()


async def mail_create__message_template_choose_cancel(callback: types.CallbackQuery):
    await mail_create_send_message_detail(callback=callback)


async def mail_create__cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    await menu(callback)


async def message_template_pagination(callback: types.CallbackQuery):
    page = int(callback.data.replace('message_template_next_page#', '').replace('message_template_prev_page#', ''))

    user_id = callback.from_user.id

    await callback.answer(_('Страница {}').format(page))
    channel_list_menu_inline_keyboard = await get_message_template_list_inline_keyboard(user_id, page)
    if callback.message.reply_markup != channel_list_menu_inline_keyboard:
        await callback.message.edit_reply_markup(channel_list_menu_inline_keyboard)


# Создать рассылку - обработка данных - отмена
async def mail_create__data_cancel(callback: types.CallbackQuery, state: FSMContext):
    """
    Отменяет заполнение того или иного поля
    """
    await state.reset_state(False)
    await mail_create_send_message_detail(callback=callback)


# Создать рассылку - изображение
async def mail_create__image(callback: types.CallbackQuery):
    await callback.message.delete()

    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()

    await callback.message.answer(_('Отправьте изображение или видео'),
                                  reply_markup=mail_create_data_cancel_inline_keyboard)
    await MailState.image_id.set()


# Создать рассылку - обработка изображения
async def mail_create__image_handler(message: types.Message, state: FSMContext):
    photo_sizes = message.photo
    video = message.video

    if photo_sizes:
        mail_image_id = photo_sizes[-1].file_id  # [-1] - самый лучший размер
        mail_video_id = None
        await state.update_data(image_id=mail_image_id, video_id=mail_video_id)
    elif video:
        mail_image_id = None
        mail_video_id = video.file_id
        await state.update_data(image_id=mail_image_id, video_id=mail_video_id)

    await state.reset_state(False)
    await mail_create_send_message_detail(message=message)


# Создать рассылку - заголовок
async def mail_create__title(callback: types.CallbackQuery):
    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()
    if callback.message.content_type in ['photo', 'video']:
        await callback.message.edit_caption(_('Отправьте заголовок'),
                                            reply_markup=mail_create_data_cancel_inline_keyboard)
    else:
        await callback.message.edit_text(_('Отправьте заголовок'), reply_markup=mail_create_data_cancel_inline_keyboard)
    await MailState.title.set()


# Создать рассылку - обработка заголовка
async def mail_create__title_handler(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.reset_state(False)
    await mail_create_send_message_detail(message=message)


# Создать рассылку - текст
async def mail_create__text(callback: types.CallbackQuery):
    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()
    if callback.message.content_type in ['photo', 'video']:
        await callback.message.edit_caption(_('Отправьте текст'), reply_markup=mail_create_data_cancel_inline_keyboard)
    else:
        await callback.message.edit_text(_('Отправьте текст'), reply_markup=mail_create_data_cancel_inline_keyboard)
    await MailState.text.set()


# Создать рассылку - обработка текста
async def mail_create__text_handler(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.reset_state(False)

    await mail_create_send_message_detail(message=message)


# Создать рассылку - кнопка
async def mail_create__button(callback: types.CallbackQuery):
    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()
    if callback.message.content_type in ['photo', 'video']:
        await callback.message.edit_caption(_('Отправьте кнопку в следующем формате:\n`Text - URL`'),
                                            reply_markup=mail_create_data_cancel_inline_keyboard,
                                            parse_mode='markdown')
    else:
        await callback.message.edit_text(_('Отправьте кнопку в следующем формате:\n`Text - URL`'),
                                         reply_markup=mail_create_data_cancel_inline_keyboard,
                                         parse_mode='markdown')
    button_number = callback.data.replace('mail_create__button', '').replace('mail_update__button', '')
    await MailState.set_button_state_by_number(button_number)


# Создать рассылку - обработка кнопки
async def mail_create__button_handler(message: types.Message, state: FSMContext):
    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()
    if ' - ' not in message.text:
        await message.answer(_('Неверный формат. Отправьте кнопку в следующем формате:\n`Text - URL`'),
                             reply_markup=mail_create_data_cancel_inline_keyboard, parse_mode='markdown')
        return
    url = message.text.split(' - ')[1]
    if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('tg://'):
        await message.answer(_('Неверный формат. Отправьте кнопку в следующем формате:\n`Text - URL`'),
                             reply_markup=mail_create_data_cancel_inline_keyboard, parse_mode='markdown')
        return

    await MailState.update_button_data_by_state(state, message.text)
    await state.reset_state(False)

    await mail_create_send_message_detail(message=message)


# Создать рассылку - выбор времени
async def mail_create__time_to_mail(callback: types.CallbackQuery):
    mail_create_data_cancel_inline_keyboard = get_mail_create_data_cancel_inline_keyboard()
    if callback.message.content_type in ['photo', 'video']:
        await callback.message.edit_caption(_('Отправьте время в формате: число;часы;минуты'),
                                            reply_markup=mail_create_data_cancel_inline_keyboard)
    else:
        await callback.message.edit_text(_('Отправьте время в формате: число;часы;минуты'),
                                         reply_markup=mail_create_data_cancel_inline_keyboard)
    await MailState.time_to_mail.set()


# Создать рассылку - обработка выбора времени
async def mail_create__time_to_mail_handler(message: types.Message, state: FSMContext):
    time_to_mail = message.text
    await state.update_data(time_to_mail=time_to_mail)
    await state.reset_state(False)

    await mail_create_send_message_detail(message=message)


async def mail_send(callback: types.CallbackQuery, state: FSMContext):
    mail_data = await state.get_data()
    time_to_mail = mail_data.get('time_to_mail')
    print(time_to_mail)

    await menu(callback)
    await state.finish()

    if time_to_mail:
        time_to_mail = time_to_mail.split(';')

        now = datetime.now()
        year = now.year
        month = now.month
        day = int(time_to_mail[0])
        hour = int(time_to_mail[1])
        minute = int(time_to_mail[2])

        eta = datetime(year, month, day, hour, minute) - timedelta(hours=3)

        await callback.answer(_('Рассылка запланирована'))

        task_mail.apply_async((mail_data, ), eta=eta)
    else:
        # print(mail_data)
        # await mail(mail_data)
        await callback.answer(_('Рассылка запущена'))

        task_mail.delay(mail_data)


async def order_send(callback: types.CallbackQuery):
    await callback.answer(_('Заказы отправляются'))

    await menu(callback)
    task_notify.delay()
