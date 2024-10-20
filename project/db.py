from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = f'postgresql+psycopg2://{str(settings.db_user)}:{str(settings.db_pass)}@{str(settings.db_host)}:{str(settings.db_port)}/{str(settings.db_name)}'

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine, expire_on_commit=False)

def get_db_session():
    with session_local() as session:
        yield session

