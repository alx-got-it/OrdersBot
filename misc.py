import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cfg import TOKEN

import os.path

package_dir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(package_dir, 'db.db')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)