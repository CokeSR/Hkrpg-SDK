import pymysql

from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig
from src.system.rebuild.database    import rebuildData

def checkMysqlConn() -> bool:
    config = getConfig()['Database']['mysql']
    ip = config['host']
    users = config['user']
    default_port = config['port']           # 3306
    default_passwd = config['password']
    default_database = config['db_name']
    try:
        # jdbc:mysql://[host]:[port]/[database]?[parameters]
        logger.info(f"Load URL 'jdbc:mysql://{ip}:{default_port}/{default_database}?user={users}&password={default_passwd}'")
        logger.info(f"Try to connect database: {config['db_name']}...")
        conn = pymysql.connect(
            host = ip,
            user = users,
            port = default_port,
            password = default_passwd,
            database = config['db_name']
        )
        if conn:
            logger.info(f"{'=' * 15} LOADING DB SUCC {'=' * 15}")
            return True
    except Exception as err:
        if "1049" in str(err):           # 1049: Unknown database
            if config['auto_rebuild']:
                logger.warning(f"Not found db_name: {default_database}, The auto_rebuild is enable...")
                logger.warning(f"Try to rebuild db: {default_database}")
                if rebuildData():
                    return True
                else:
                    return False
            else:
                logger.warning(f"Not found db_name: {default_database}, The auto_rebuild is disable...")
                logger.warning(f"Please make sure your database is exists.")
                return False
        else:
            logger.error(err)
            return False
