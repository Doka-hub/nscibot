from aiogram import Dispatcher

# local imports
from .is_admin import AdminFilter, AdminCallbackDataFilter
from .whitelist import WhiteListFilter
from .callback import CallbackData, CallbackDataStartsWith


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(WhiteListFilter)
    dp.filters_factory.bind(CallbackData)
    dp.filters_factory.bind(CallbackDataStartsWith)
    dp.filters_factory.bind(AdminCallbackDataFilter)

