from misc import dp, bot
from filters import is_auth, check_user
from datetime import datetime
from states.register_states import register
from aiogram import types
from aiogram.dispatcher import FSMContext

from methods.insert import User,SellerAccount
from methods.get_data import select_seller_accounts
from cfg import admins

import requests

@dp.callback_query_handler()
async def parse_poz(call: types.CallbackQuery):
    if call.data == 'registration':
        u = check_user(user_id = call.from_user.id)
        сheck = u.check_reg_user()
        if сheck == True:
            await call.message.answer('Вы уже зарегистрированы!')
        else:
            await call.message.answer('Для дальнейшего использования, укажите ключ API (Статистика) вашего магазина. Получить его можно в личном кабинете: Настройки - Доступ к API - Создать новый токен - Статистика')
            await register.api_key.set()
    
    elif call.data == 'check_users_count':
        if call.from_user.id in admins:
            n = len(select_seller_accounts())
            await call.message.edit_text(f'Количество пользователей:{n}')
        else:
            pass
        
        
        
@dp.message_handler(is_auth(),commands='registration')
async def process_reg_command(message: types.Message):
    await message.answer('Для дальнейшего использования, укажите ключ API (Статистика) вашего магазина. Получить его можно в личном кабинете: Настройки - Доступ к API - Создать новый токен - Статистика')
    await register.api_key.set()


@dp.message_handler(is_auth(),commands='add_account')
async def process_add_account_command(message: types.Message):
    await register.seller_url.set()


@dp.message_handler(state=register.seller_url, content_types=['any'])
async def seller_url(message: types.Message, state: FSMContext):
    if message.text.lower() in ['отмена','назад']:
        await message.answer('Отменено')
        await state.finish()
    else:
        if message.text.startswith('https://www.wildberries.ru/'):
            await state.update_data(seller_url=message.text)
            await message.answer('Далее, для сбора информации, нам понадобится Wildberries API KEY (Статистика)')
            await register.api_key.set()
        else:
            await message.answer('Это не похоже на ссылку! Попробуйте снова.')


@dp.message_handler(state=register.api_key, content_types=['any'])
async def api_key(message: types.Message, state: FSMContext):
    if message.text.lower() in ['отмена','назад']:
        await message.answer('Отменено')
        await state.finish()
    else:
        await state.update_data(api_key=message.text)

        data = await state.get_data()
        now = datetime.now()
        r = requests.get(url='https://statistics-api.wildberries.ru/api/v1/supplier/stocks', headers={"Authorization": data['api_key']}, params={'dateFrom':now}).status_code
        if r == 200:
        
            user = SellerAccount(user_id=message.from_user.id, user_name=message.from_user.username,
                                 seller_url=None, api_key=data['api_key'])
    
            user.add_user()
            user.add_seller_account()
    
            await message.answer('Спасибо! Ожидайте уведомлений!')
            await state.finish()
        else:
            await message.answer('Апи ключ не действителен, пожалуйста, проверьте его и повторите попытку!')
        
        

