from aiogram.dispatcher.filters.state import State, StatesGroup


class ProviderState(StatesGroup):
    """
    When admin click to "add vk" button, his states set to S_ENTER_VK_PAGE
    """
    user_id = State()
    vk_link = State()


class UserState(StatesGroup):
    """
    To identify a supplier, we need his phone number
    """
    S_DEFAULT = State()
    S_ENTER_PHONE_NUMBER = State()


class SubscribeState(StatesGroup):
    """
    To subscribe to a vibe bot, a user must send any message
    """
    S_DEFAULT = State()
    S_ENTER_TEXT = State()
