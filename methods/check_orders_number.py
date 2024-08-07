from models import orders
from database import engine
from sqlalchemy import select,insert

class Order:
    def __init__(self, order_id,user_id):
        self.order_id = order_id
        self.user_id = user_id

    def add_order(self):
        ord = insert(orders).values(
            order_id = self.order_id,
            user_id = self.user_id
        )
        try:
            conn = engine.connect()
            r = conn.execute(ord)
            conn.commit()
        except:
            pass

    def check_order(self):
        conn = engine.connect()
        s = select(orders).where(
            orders.c.order_id == str(self.order_id)
        )
        rs = conn.execute(s)
        if rs.fetchone():
            return True
        else:
            return False
