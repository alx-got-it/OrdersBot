from aiogram.dispatcher.filters.state import StatesGroup, State

class register(StatesGroup):
    api_key = State()
    seller_url = State()