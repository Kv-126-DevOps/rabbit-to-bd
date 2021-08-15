import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


def getEnvVariable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected env variable {name} not set."
        raise Exception(message)


POSTGRES_HOST = getEnvVariable("POSTGRES_HOST")
POSTGRES_PORT = getEnvVariable("POSTGRES_PORT")
POSTGRES_USER = getEnvVariable("POSTGRES_USER")
POSTGRES_PW = getEnvVariable("POSTGRES_PW")
POSTGRES_DB = getEnvVariable("POSTGRES_DB")

MYSQL_HOST = getEnvVariable("MYSQL_HOST")
MYSQL_PORT = getEnvVariable("MYSQL_PORT")
MYSQL_USER = getEnvVariable("MYSQL_USER")
MYSQL_PW = getEnvVariable("MYSQL_PW")
MYSQL_DB = getEnvVariable("MYSQL_DB")

MSSQL_HOST = getEnvVariable("MSSQL_HOST")
MSSQL_PORT = getEnvVariable("MSSQL_PORT")
MSSQL_USER = getEnvVariable("MSSQL_USER")
MSSQL_PW = getEnvVariable("MSSQL_PW")
MSSQL_DB = getEnvVariable("MSSQL_DB")

RABBIT_HOST = getEnvVariable("RABBIT_HOST")
RABBIT_PORT = getEnvVariable("RABBIT_PORT")
RABBIT_USER = getEnvVariable("RABBIT_USER")
RABBIT_PW = getEnvVariable("RABBIT_PW")
RABBIT_QUEUE = getEnvVariable("RABBIT_QUEUE")


POSTGRES_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
MYSQL_URL = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PW}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
MSSQL_URL = f'mssql+pymssql://{MSSQL_USER}:{MSSQL_PW}@{MSSQL_HOST}:{MSSQL_PORT}/{MSSQL_DB}'

DB_URL = POSTGRES_URL

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'HelloWorld'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
