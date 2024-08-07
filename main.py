from aiogram import executor

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from misc import dp,bot
from functions import start as parse

import handlers
import filters
import methods

from cfg import admins

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler.add_job(handlers.on_startup.on_start, trigger='interval', minutes=5, kwargs={'bot':bot})
scheduler.start()


if __name__ == '__main__':
    filters.setup(dp)
    executor.start_polling(dp,skip_updates=True)