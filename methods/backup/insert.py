import sqlite3
from aiogram import types
from misc import database_path as db

class User:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name


    def add_user(self):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO users (user_id, user_name) VALUES (?,?)', (self.user_id, self.user_name,))

        connection.commit()
        connection.close()

class SellerAccount(User):

    def __init__(self, user_id, user_name, seller_url=None, api_key=None):
        super().__init__(user_id, user_name)
        self.seller_url = seller_url
        self.api_key = api_key

    def add_seller_account(self):

        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO seller_accounts (user_id, seller_url, api_key) VALUES (?,?,?)', (self.user_id, self.seller_url, self.api_key))

        connection.commit()
        connection.close()

    # def update_wb_url(self):
    #     connection = sqlite3.connect(db)
    #     cursor = connection.cursor()
    #
    #     cursor.execute('UPDATE seller_accounts SET seller_url = ? WHERE id = ?', (self.seller_url, self.user_id))
    #
    #     connection.commit()
    #     connection.close()
    #
    # def update_api_key(self):
    #     ...
