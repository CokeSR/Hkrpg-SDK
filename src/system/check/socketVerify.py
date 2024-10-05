from OpenSSL                        import crypto
from datetime                       import datetime
from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig


import src.system.response.retcode  as path


def checkSSL() -> bool:
    config = getConfig()['App']
    if config['ssl']:
        # 读取ssl
        try:
            with open(path.SSL_PEM_PATH, 'r', encoding="UTF-8") as file:
                ssl_pem = file.read()
                logger.info("Load ssl file succ: {}".format(ssl_pem.replace('\n',"")))
        except Exception as err:
            logger.error(f"Read ssl file fail: {err}")
            return False
        # 验证
        try:
            now        = datetime.utcnow()
            cert       = crypto.load_certificate(crypto.FILETYPE_PEM, ssl_pem)
            not_before = datetime.strptime(cert.get_notBefore().decode("ascii"), "%Y%m%d%H%M%SZ")
            not_after  = datetime.strptime(cert.get_notAfter().decode("ascii"), "%Y%m%d%H%M%SZ")
            if not_before <= now <= not_after:
                # 有效
                logger.info(f"Load ssl socket succ: The certificate is valid")
                # 是否自签 不阻塞
                if cert.get_subject() == cert.get_issuer():
                    logger.warning(f"The certificate is self-signed")
                    return True
                else:
                    logger.info(f"The certificate is issued by a trusted ERASER")
                    return True
            else:
                # 无效证书
                logger.error(f"Load ssl socket failed: The certificate is not valid")
                # 未生效
                if now < not_before:
                    logger.error(f"The certificate has not yet taken effect")
                    return False
                # 过期
                elif now > not_after:
                    logger.error(f"The certificate has expired")
                    return False
                
                return False
        except Exception as err:
            logger.error(f"Try to verify ssl config failed: {err}")
            return False
    else:
        logger.warning(f"Not enable SSL socket conn, skipping check")
        return True
