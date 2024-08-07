import sqlite3
from misc import database_path as db

class GetData():
    def outer():
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        cursor.execute('SELECT user_id,seller_url,api_key FROM seller_accounts')
        accounts = cursor.fetchall()

        connection.close()

        return accounts