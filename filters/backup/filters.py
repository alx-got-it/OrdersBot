from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from cfg import admins
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import sqlite3


class is_auth(BoundFilter):
    async def check(self, message: types.Message):

        connection = sqlite3.connect('db.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id == ?', (message.from_user.id,))
        user = cursor.fetchone()

        connection.close()

        if user == None:
            return True
        else:
            await message.answer('Вы уже зарегистрированы!')

class cansel(BoundFilter):
    async def check(self, message: types.Message, state: FSMContext):
        if message.text.lower() == 'отмена' or message.text.lower() == 'назад':
            await message.answer('Отменено!')
            await state.finish()
            return False
        else:
            return True