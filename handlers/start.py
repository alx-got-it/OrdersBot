from misc import dp
from misc import bot
from aiogram import types
from cfg import admins
from functions import start as parse
from markup.keyboard import reg, admin_panel

@dp.message_handler(commands="start")
async def process_start_command(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(f'Привет, {message.from_user.username}!')
    else:
        await message.answer('Привет, селлер!\nМеня зовут username, я больше 3 лет продаю на Ozon и Wildberries. Выручка за прошлый год составила 180 млн рублей. \n\nУ себя в канале я подготовил для тебя подарок: серия постов про продвижение карточки товара на WB. Читай вот тут\n\nhttps://t.me/xoxlov_maxim/967\n\n☝️Не забудь подписаться на канал, Там очень много всего интересного. \n\nМы с командой разработали данного бота для вас. Он бесплатный и несёт в себе полезные функции для более удобной работы с Wildberries 🚀\n\nНажимай "Регистрация", чтобы начать работу с ботом 👇', reply_markup=reg())

@dp.message_handler(commands="admin")
async def process_start_command(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(f'Привет, {message.from_user.username}!', reply_markup=admin_panel())
    else:
        pass