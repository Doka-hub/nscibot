from aiogram import types

# local imports
from utils.bot.db_api.admin.whitelist import add_to_whitelist_, remove_from_whitelist_

from loader import bot_i18n_gettext as _


async def add_to_whitelist(message: types.Message):
    user_id = message.get_args()

    if user_id.isdigit():
        await add_to_whitelist_(int(user_id))
        await message.answer(_('{} добавлен в whitelist').format(user_id))
    else:
        await message.answer(_('Неверный id'))


async def remove_from_whitelist(message: types.Message):
    user_id = message.get_args()
    if user_id.isdigit():
        await remove_from_whitelist_(int(user_id))
        await message.answer(_('{} удалён из whitelist').format(user_id))
    else:
        await message.answer(_('Неверный id'))
