from aiogram import Dispatcher

# local imports
from . import admin, errors, user


def setup(dp: Dispatcher):
    admin.setup(dp)
    errors.setup(dp)
    user.setup(dp)
