import smtplib
from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig

def checkEmailConn() -> bool:
    config = getConfig()['Mail']
    
    status     = config['enable']
    name       = config['mail_username']
    port       = config['mail_port']
    password   = config['mail_pasword']
    ip_address = config['mail_server']
    
    if status:
        try:
            logger.info(f"Load user: {name} , password: {password} , Try to connect email_server: {ip_address}:{port}")
            
            server = smtplib.SMTP(ip_address, port)
            server.starttls()
            server.login(name, password)
            
            if server:
                logger.info(f"{'=' * 15} CONNECT EMAIL SERVICE SUCC {'=' * 15}")
                server.close()
                return True
            
        except Exception as err:
            logger.error(f"{err}. Please check your Email config and make sure user or password correct.")
            return False

    else:
        logger.info(f"Load user: {name} , password: {password}, email_server: {ip_address}:{port}")
        logger.warning(f"The email model is disable, skip check...")
        logger.warning(f"{'=' * 15} CONNECT EMAIL SERVICE SKIP {'=' * 15}")
        return True
