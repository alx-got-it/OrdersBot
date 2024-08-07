from sqlalchemy import select
from database import engine
from models import seller_accounts

def select_seller_accounts():

    conn = engine.connect()
    s = select(seller_accounts)
    rs = conn.execute(s)

    return rs.fetchall()


