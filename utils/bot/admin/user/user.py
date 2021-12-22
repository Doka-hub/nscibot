from typing import Optional, List, Union

# local imports
from models.bot import objects, TGUser


async def get_or_create_user(user_id: int, username: Optional[str] = None) -> List[Union[TGUser, bool]]:
    user, created = await objects.get_or_create(TGUser, user_id=user_id)

    # если юзернейм указан и он не является настоящим юзернеймом (а новым)
    if username and user.username != username:
        user.username = username
        await objects.update(user, ['username'])
    return [user, created]


async def get_user_list() ->List[TGUser]:
    user_list = await objects.execute(TGUser.select().where(TGUser.bot_blocked_by_user == False))
    return user_list
