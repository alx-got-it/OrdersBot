from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
    
def reg():
    registration = InlineKeyboardButton('Регистрация', callback_data='registration')
    markup = InlineKeyboardMarkup().add(registration)
    return markup


def admin_panel():
    check_users_count = InlineKeyboardButton(text='Подключить аккаунт', callback_data='check_users_count')
    
    
    markup = InlineKeyboardMarkup().add(check_users_count)

    return markup