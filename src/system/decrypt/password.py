import platform
import bcrypt
import hashlib

from src.system.logging.systemctl import logger

def password_hash(password) -> str:
    sys_platfrom = platform.system()
    logger.info(f"Try encrypt password: {password}")
    # 如果是 Windows 平台部署 不进行加密
    if sys_platfrom == "Windows":
        logger.info(f"Encrypt password succ: {password}")
        return password
    try:
        h = hashlib.new("sha256")
        h.update(password.encode())
        logger.info(f"Encrypt password succ: {password}")
        return bcrypt.hashpw(h.hexdigest().encode(), bcrypt.gensalt())
    except Exception as err:
        logger.error(f"Encrypt password fail, return origin passwd: {err}")
        return password


# 密码验证
def password_verify(password, hashed) -> str:
    h = hashlib.new("sha256")
    h.update(password.encode())
    return bcrypt.checkpw(h.hexdigest().encode(), hashed.encode())
