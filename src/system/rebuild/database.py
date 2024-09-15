import pymysql
from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig

def rebuildData() -> bool:
    config = getConfig()['Database']['mysql']
    db_name = config['db_name']
    
    conn = pymysql.connect(
        host = config['host'],
        user = config['user'],
        port = config['port'],
        password = config['password'],
        autocommit = True
    )
    
    try:
        cursor = conn.cursor()
        sql_data = [
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8 COLLATE utf8_general_ci;",
            f"USE `{db_name}`;",
            f"DROP TABLE IF EXISTS `t_accounts`;",
            f"DROP TABLE IF EXISTS `t_accounts_tokens`;",
            f"DROP TABLE IF EXISTS `t_accounts_guests`;",
            f"DROP TABLE IF EXISTS `t_combo_tokens`;"
        ]
        
        for cmd in sql_data:
            logger.info(f"Run command: {cmd}")
            cursor.execute(cmd)

        logger.info(f"Rebuild {db_name}.t_accounts")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `t_accounts` (
                `uid` INT AUTO_INCREMENT PRIMARY KEY COMMENT '玩家UID',
                `name` VARCHAR(255) COMMENT '用户名',
                `mobile` VARCHAR(255) UNIQUE COMMENT '手机号',
                `email` VARCHAR(255) UNIQUE COMMENT '电子邮件',
                `password` VARCHAR(255) COMMENT '哈希密码',
                `type` INT NOT NULL COMMENT '1 注册 0 未注册',
                `epoch_created` INT NOT NULL COMMENT '时间戳'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            COMMENT='玩家账号信息表'
            """
        )
        
        logger.info(f"Rebuild {db_name}.t_accounts_tokens")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `t_accounts_tokens` (
                `uid` INT NOT NULL COMMENT '玩家UID',
                `token` VARCHAR(255) NOT NULL COMMENT '登录Token',
                `device` VARCHAR(255) DEFAULT NULL COMMENT '设备ID',
                `ip` VARCHAR(255) NOT NULL COMMENT '登录IP',
                `epoch_generated` INT NOT NULL COMMENT '时间戳',
                PRIMARY KEY(`uid`,`token`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            COMMENT='账号登录token'
            """
        )
        
        logger.info(f"Rebuild {db_name}.t_accounts_guests")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `t_accounts_guests` (
                `uid` INT NOT NULL COMMENT '玩家UID',
                `device` VARCHAR(255) NOT NULL COMMENT '设备ID',
                PRIMARY KEY(`uid`,`device`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            COMMENT='游客登录信息表'
            """
        )

        logger.info(f"Rebuild {db_name}.t_combo_tokens")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `t_combo_tokens` (
                `uid` INT NOT NULL COMMENT '玩家UID',
                `token` VARCHAR(255) NOT NULL COMMENT '登录Token',
                `device` VARCHAR(255) NOT NULL COMMENT '设备ID',
                `ip` VARCHAR(255) NOT NULL COMMENT '登录IP',
                `epoch_generated` INT NOT NULL COMMENT '时间戳',
                PRIMARY KEY(`uid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
            COMMENT='设备信息token'
            """
        )
        
        logger.info(f"{'=' * 15} REBUILD DATABASE SUCC {'=' * 15}")
        conn.close()
        return True
    except Exception as err:
        logger.error(f"{'=' * 15} REBUILD DATABASE FAILED {'=' * 15}")
        logger.error(f"Error msg: {err}")

        cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")
        conn.close()
        return False
