from aiogram import Dispatcher

# local imports
from . import errors, admin, user


def setup(dp: Dispatcher):
    errors.setup(dp)
    admin.setup(dp)
    user.setup(dp)
