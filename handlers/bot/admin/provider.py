from aiogram import types
from aiogram.dispatcher.storage import FSMContext

# local imports
from states.bot.admin import ProviderState

from utils.bot.db_api.user import get_or_create_user, set_user__vk_link

from loader import bot_i18n_gettext as _, provider_dp


async def provider__vk_link_set(callback: types.CallbackQuery):
    """
    Добавляем страницу ВК юзеру
    :param callback:
    :return:
    """

    '''callback.data = "admin_provider_vk_link_set 24" (24 - provider_user_id)'''
    provider_user_id = callback.data.replace('admin_provider_vk_link_set ', '')

    await provider_dp.storage.set_data(user=callback.from_user.id, data={'user_id': provider_user_id})

    await ProviderState.vk_link.set()
    await callback.message.answer(_('Введите ссылку на страницу в ВК, например: \n'
                                    '`https://vk.com/ajour7km`'), parse_mode='markdown')


def provider__vk_link_set_handler(message: types.Message, state: FSMContext):
    vk_link = message.text

    data = await state.get_data()
    provider_user_id = data.get('user_id')

    if 'vk.com' not in vk_link:
        message.answer(_('Ссылка, которую вы ввели не содержит vk.com, '
                         'введите пожалуйста ссылку в таком формате: \n'
                         '`https://vk.com/ajour7km`'), parse_mode='markdown')
    else:
        provider, provider_created = await get_or_create_user(provider_user_id)
        await set_user__vk_link(provider, vk_link)
        message.answer(_('Вы успешно обновлили группу для сбора товаров поставщика, '
                         'теперь на сайте появятся его товары 👍'))
        await state.finish()
