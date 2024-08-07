from sqlalchemy import create_engine, select, insert
from settings import settings
from models import users,seller_accounts,orders

engine = create_engine(
    url = settings.DATABASE_URL,
    echo=True, pool_size=20, max_overflow=60,
)


