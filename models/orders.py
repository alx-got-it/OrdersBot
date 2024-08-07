from sqlalchemy import (
    MetaData,
    Table,
    String,
    Integer,
    Column,
    Text,
    DateTime,
    Boolean,
    Numeric,
    BigInteger,
    create_engine,
)
from settings import settings

engine = create_engine(
    url=settings.DATABASE_URL,
    echo=True,
    pool_size=6,
    max_overflow=10,
)
conn = engine.connect()
metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("id", BigInteger(), primary_key=True),
    Column("order_id", Text()),
    Column("user_id", Numeric()),
)
metadata.create_all(engine)
