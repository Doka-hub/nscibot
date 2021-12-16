from aiogram import types
from aiogram.types import reply_keyboard

# local imports
from data import config

from keyboards.bot.default.user import get_request_contact_default_keyboard
from keyboards.bot.inline.user import (
    get_menu_inline_keyboard, get_balance_inline_keyboard, get_more_inline_keyboard,
    get_news_inline_keyboard,
    get_referral_inline_keyboard, get_back_to_menu_inline_keyboard
)

from utils.bot.db_api.user import (
    get_or_create_user, 
    get_user_referral_list, format_referral_list,
    get_exchange_rate as get_exchange_rate_
)
from utils.bot.set_commands import set_commands

from loader import bot_i18n_gettext as _, bot


async def menu(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    user_id = callback.from_user.id
    username = callback.from_user.username or None
    
    menu_inline_keyboard = get_menu_inline_keyboard(user_id=user_id)
    await callback.message.answer(_('Меню'), reply_markup=menu_inline_keyboard)


async def balance(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    
    user_id = callback.from_user.id
    username = callback.from_user.username or None
    user, user_created = await get_or_create_user(user_id, username)

    balance_inline_keyboard = get_balance_inline_keyboard(user_id=user_id)
    await callback.message.answer(_(
        f'''Баланс: {user.balance} NSCI
Примерно: {user.balance * 10} RUB
🤝 Приглашено: {user.referral_cabinet.get().referrals.count()} пользователей
💰 Заработано: {user.earned} NSCI
        '''
    ), reply_markup=balance_inline_keyboard)


async def withdraw(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or None
    
    await callback.answer(_('Временно не доступно'))


async def referral(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    
    user_id = callback.from_user.id
    username = callback.from_user.username or None
    user, user_created = await get_or_create_user(user_id, username)

    referral_inline_keyboard = get_referral_inline_keyboard()
    await callback.message.answer(_(
        f'''💵 Партнерская программа 🤝
Реферальная программа 2 уровней
1)	2% - получайте 2% от покупок ваших друзей
2)	8% - По достижению 10 друзей, которые приобрели NSCI для себя, вы будете получать 8% от их покупок
Приглашайте новых пользователей и получайте пассивный доход от комиссий бота! 💵 
Реферальная программа бессрочна, не имеет лимита приглашений и начинает действовать моментально.
Для достижения высоких результатов, внимательно подходите к поиску целевой аудитории: привлекайте только тех, кто будет покупать или продавать криптовалюту.
Используйте уникальную реферальную ссылку для приглашения пользователей. Чеки и ссылки на ваши объявления также являются реферальными.
t.me/NSCI_Venture_Bot?start={user.referral_cabinet.get().referral_link}
        '''), reply_markup=referral_inline_keyboard
    )

async def referral_list(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    
    user_id = callback.from_user.id
    username = callback.from_user.username or None
    user, user_created = await get_or_create_user(user_id, username)

    user_referral_list = await get_user_referral_list(user)
    text = await format_referral_list(user_referral_list)
    back_to_menu_inline_keyboard = get_back_to_menu_inline_keyboard()
    await callback.message.answer(_(f'Ваши рефераллы: \n{text}'), reply_markup=back_to_menu_inline_keyboard)


async def more(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    
    user_id = callback.from_user.id
    username = callback.from_user.username or None

    more_inline_keyboard = get_more_inline_keyboard()
    await callback.message.answer(_('Дополнительно'), reply_markup=more_inline_keyboard)


async def news(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    user_id = callback.from_user.id
    username = callback.from_user.username or None
    
    news_inline_keyboard = get_news_inline_keyboard()
    await callback.message.answer(_('Новости'), reply_markup=news_inline_keyboard)


async def get_exchange_rate(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or None

    exchange_rate = await get_exchange_rate_()
    await callback.message.answer(exchange_rate)
    return
