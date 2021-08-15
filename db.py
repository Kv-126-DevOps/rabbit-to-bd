from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from config import *
from models import Base

isConnected = False

try:
    # Drop db
    # if database_exists(DB_URL):
    #     drop_database(DB_URL)

    # Create db
    if not database_exists(DB_URL):
        create_database(DB_URL)

    # Create tables
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    isConnected = True
except OperationalError as ex:
    print(ex)
