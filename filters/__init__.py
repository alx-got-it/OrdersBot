from aiogram import Dispatcher

from .filters import is_auth, cansel, check_user


def setup(dp: Dispatcher):
    dp.filters_factory.bind(is_auth)
    dp.filters_factory.bind(cansel)