import asyncio
import time
import os, shutil

from misc import dp, bot
from filters import is_auth
from functions import photos
from states.register_states import register
from aiogram import types
from aiogram.dispatcher import FSMContext

from os.path import isfile, join
from methods.insert import User,SellerAccount
import aiohttp
import aiofiles
from functions import start as parse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cfg import admins


async def splitter(numb):
    numb = str(numb)
    if len(numb) > 3:
        result = " ".join([numb[::-1][i:i+3] for i in range(0, len(numb), 3)])[::-1]
        return result
    else:
        return numb


async def on_start(bot: bot):
    data = await parse()
    time.sleep(2)
    photo_list = []
    if data:
        for accounts in data:
            for mes in accounts:
                feedbacks = await splitter(mes['feedbacks'])

                price = await splitter(int(mes['price']))
                
                TOA = mes['today_orders_all'].split(' ')
                TOA_amount = await splitter(TOA[0])
                TOA_price = await splitter(TOA[2])

                tdT = mes['todayThis'].split(' ')
                todayThis_amount = await splitter(tdT[0])
                todayThis_price = await splitter(tdT[2])

                ydT = mes['yesterdayThis'].split(' ')
                yesterdayThis_amount = await splitter(ydT[0])
                yesterdayThis_price = await splitter(ydT[2])

                gNumber = mes['id']
                
                NoSize = ''
                Size = f"🪡Размер: {mes['techSize']}\n"
                
                text = f"🕛 {mes['date'].split('T')[0].split('-')[2]}" \
                       f".{mes['date'].split('T')[0].split('-')[1]}" \
                       f".{mes['date'].split('T')[0].split('-')[0]}" \
                       f" {mes['date'].split('T')[1]}\n" \
                       f"🛒 Заказ [{mes['number']}]: {price}₽\n" \
                       f"📈 Сегодня всего: {TOA_amount} на {TOA_price}₽\n" \
                       f"🆔 Артикул: {mes['nmId']}\n" \
                       f"{Size if mes['techSize'] != '0' else NoSize}" \
                       f"📂 {mes['subject']}\n" \
                       f"™️ {mes['brand']}\n" \
                       f"🏷 {mes['supplierArticle']}\n" \
                       f"⭐️ Рейтинг: {mes['rating']}\n" \
                       f"💬 Отзывы: {feedbacks}\n" \
                       f"⏱️ Сегодня заказов: {TOA_amount}\n" \
                       f"⏳ Сегодня таких: {todayThis_amount} на {todayThis_price}₽\n" \
                       f"⌛️ Вчера таких: {yesterdayThis_amount} на {yesterdayThis_price}₽\n" \
                       f"🌎 {mes['warehouseName']} → {mes['oblast']}\n" \
                       f"🚛 В пути до клиента: {mes['inWayToClient']}\n" \
                       f"🚚 В пути от клиента: {mes['inWayFromClient']}\n" \
                       f"📦 Остаток на складе: {mes['quantity']}"

                        #f"💎 Выкуп за 3 мес: {mes['buyouts']}\n" \

                async with aiofiles.open(f"functions/photos/{str(gNumber)}.png",
                                         mode='rb') as f: 
                    prod_photo = await f.read()
                try:
                    #await bot.send_photo(admins[0], photo=prod_photo, caption=text + f'\n\n{mes["user_id"]}')
                    await bot.send_photo(mes['user_id'], photo=prod_photo, caption=text)
                except:
                    #await bot.send_photo(admins[0], photo=f, caption=text + f'\n\n{mes["user_id"]}')
                    await bot.send_photo(mes['user_id'], photo=f, caption=text)

                photo_list.append(f'functions/photos/{str(gNumber)}.png')

    else:
        pass

    for y in set(photo_list):
        os.remove(y)