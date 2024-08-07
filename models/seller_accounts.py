from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BigInteger, Numeric

metadata = MetaData()

seller_accounts = Table('seller_accounts', metadata,
               Column('id', BigInteger(),primary_key=True),
               Column('user_id', BigInteger()),
               Column('seller_url', Text()),
               Column('api_key', Text()),
              schema=None
              )