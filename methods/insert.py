from models import users,seller_accounts
from sqlalchemy import insert, select
from database import engine

class User:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def add_user(self):
        user = insert(users).values(
            user_id = self.user_id,
            user_name = self.user_name
        )
        try:
            conn = engine.connect()
            r = conn.execute(user)
            conn.commit()
        except Exception as e:
            print(e)

class SellerAccount(User):
    def __init__(self, user_id, user_name, seller_url=None, api_key=None):
        super().__init__(user_id, user_name)
        self.seller_url = seller_url
        self.api_key = api_key

    def add_seller_account(self):
        sell_acc = insert(seller_accounts).values(
            user_id = self.user_id,
            api_key = self.api_key
        )
        try:
            conn = engine.connect()
            r = conn.execute(sell_acc)
            conn.commit()
        except Exception as e:
            print(e)
