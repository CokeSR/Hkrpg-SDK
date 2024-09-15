import pymysql
from src.system.loading.config import getConfig

def get_db() -> str:
    config = getConfig()['Database']['mysql']
    conn = pymysql.connect(
        host = config['host'],
        user = config['user'],
        port = config['port'],
        password = config['password'],
        database = config['db_name'],
        autocommit = True
    )
    return conn
