from aiogram import types

# local imports
from data import config
from handlers.bot.user.menu import referral

from keyboards.bot.default.user import get_request_contact_default_keyboard
from keyboards.bot.inline.user.language import get_language_inline_keyboard
from keyboards.bot.inline.user import get_menu_inline_keyboard

from utils.bot.db_api.user import get_or_create_user, set_referral
from utils.bot.set_commands import set_commands

from loader import bot_i18n_gettext as _, bot


@set_commands
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or None
    user, user_created = await get_or_create_user(user_id, username)
    
    referrer_id = message.get_args()
    if referrer_id and int(referrer_id) != int(user_id):
        await set_referral(user, referrer_id)

    if not user.language:
        language_inline_keyboard = get_language_inline_keyboard()
        await message.answer('Выберите язык / Choose language',
                                      reply_markup=language_inline_keyboard)
    else:
        menu_inline_keyboard = get_menu_inline_keyboard(user_id=user_id)
        await message.answer(_('Меню'), reply_markup=menu_inline_keyboard)


# # Обработка контакта
# async def contact__handler(message: types.Message):
#     delete_markup_message = await message.answer('...', reply_markup=types.ReplyKeyboardRemove())
#     await delete_markup_message.delete()

#     user_id = message.from_user.id
#     username = message.from_user.username or None
#     user, user_created = await get_or_create_user(user_id, username)

#     user_phone_number = message.contact['phone_number']
#     user_full_name = message.contact['first_name']

#     await set_user__phone_number(user, user_phone_number)
#     await set_user__full_name(user, user_full_name)

#     await message.answer(
#         _(
#             '''
#             🥳 Поздравляем! 

# Вы только-что подписались на получение информации о заказах в телеграмм, мы вас уведомим, если у вас что-нибудь закажут.
#             '''
#         )
#     )

#     for admin_id in config.ADMINS:
#         await bot.send_message(
#             admin_id,
#             _(
#                 f'''
#                 ✅ Поставщик {user_full_name} с телефоном: {user_phone_number} подписался на получение заказов

# 📝 Вы можете добавить ссылки для того, чтобы его товары попадали на сайт
#                 '''
#             )
#         )
