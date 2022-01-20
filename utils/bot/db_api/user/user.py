from typing import Optional, List, Union

# local imports
from models.bot import objects, TGUser, ReferralCabinet, ExchangeRate, DoesNotExist


async def get_or_create_user(user_id: str, username: Optional[str] = None) -> List[Union[TGUser, bool]]:
    user, created = await objects.get_or_create(TGUser, user_id=str(user_id))

    if created:
        await objects.get_or_create(ReferralCabinet, tguser=user,
                                    referral_link=str(user.user_id))
        user.balance += 10
        await objects.update(user, ['balance'])

    # если юзернейм указан и он не является настоящим юзернеймом (а новым)
    if username and user.username != username:
        user.username = username
        await objects.update(user, ['username'])
    return [user, created]


async def set_referral(referral: TGUser, referrer_id: int):
    referrer, referrer_created = await objects.get_or_create(TGUser,
                                                             user_id=str(referrer_id))
    referrer_cabinet = referrer.referral_cabinet.get()
    if referral not in referrer_cabinet.referrals:
        referrer_cabinet.referrals.add([referral])
        
        referral.is_referral = True
        referral.referrer_user_id = referrer.id
        await objects.update(referral, ['is_referral', 'referrer_user_id'])


async def get_or_none_by_phone_number(phone_number: str) -> Optional[TGUser]:
    try:
        user = await objects.get(TGUser, phone_number=phone_number)
    except DoesNotExist:
        user = None
    return user


async def get_user_list(*expressions) -> List[TGUser]:
    expressions = (
        TGUser.bot_blocked_by_user == False, TGUser.is_active == True,
        *expressions
    )
    user_list = await objects.execute(TGUser.select().where(*expressions))
    return user_list


async def get_user_referral_list(user: TGUser) -> List[TGUser]:
    user_referral_list = await objects.execute(user.referral_cabinet.get().referrals)
    return user_referral_list


async def format_referral_list(referral_list: List[TGUser]) -> str:
    text = ''
    for referral in referral_list:
        text += f'{referral.username or referral.user_id} - {await referral.get_bought_amount()}\n'
    return text


async def get_exchange_rate() -> int:
    exchange_rate = (await objects.execute(ExchangeRate.select()))[0]
    return exchange_rate.cost


async def set_user__phone_number(user: TGUser, phone_number: str):
    user.phone_number = phone_number
    await objects.update(user, ['phone_number'])


async def set_user__full_name(user: TGUser, full_name: str):
    user.full_name = full_name
    await objects.update(user, ['full_name'])


async def set_user__vk_link(user: TGUser, vk_link: str):
    user.vk_link = vk_link
    await objects.update(user, ['vk_link'])

