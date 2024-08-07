from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from aiogram.dispatcher import FSMContext

from sqlalchemy import select
from models import users
from database import engine

class check_user:
    def __init__(self, user_id):
        self.user_id = user_id

    def check_reg_user(self):
        conn = engine.connect()
        s = select(users).where(users.c.user_id == self.user_id)
        rs = conn.execute(s)
        user = rs.fetchall()
        print('USER: ...',user)
        if user:
            return True
        else:
            return False
            
            
class is_auth(BoundFilter):
    async def check(self, message: types.Message):
        conn = engine.connect()
        s = select(users).where(users.c.user_id == self.user_id)
        rs = conn.execute(s)
        user = rs.fetchall()
        print('USER: ...',user)
        if user:
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