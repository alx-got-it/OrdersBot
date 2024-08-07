from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, BigInteger, Numeric

metadata = MetaData()

users = Table('users', metadata,
               Column('id', BigInteger(),primary_key=True),
               Column('user_id', BigInteger()),
               Column('user_name', Text()),
              schema=None
              )