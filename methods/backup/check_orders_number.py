import asyncio
import sqlite3
import aiosqlite
from misc import database_path as db

class Order:
    def __init__(self, order_id,user_id):
        self.order_id = order_id
        self.user_id = user_id

    async def add_order(self):
        try:
            connection = await aiosqlite.connect(db)
            cursor = await connection.cursor()

            await cursor.execute('INSERT INTO orders (order_id, user_id) VALUES (?,?)', (self.order_id, self.user_id,))

            await connection.commit()
            await connection.close()

            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(e)
            return False

    async def check_order(self,order):
        connection = await aiosqlite.connect(db)
        cursor = await connection.cursor()

        await cursor.execute('SELECT id FROM orders WHERE order_id = ?', [order])
        y = await cursor.fetchone()
        await connection.commit()
        await connection.close()

        if y:
            return True
        else:
            return False
