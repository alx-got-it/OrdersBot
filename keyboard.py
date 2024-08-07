from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


registration = InlineKeyboardButton('Регистрация', callback_data='registration')
menu = InlineKeyboardMarkup().add(registration)