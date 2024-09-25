# 接口鉴权
# rsa(base64(sign + timestamp + cmd))
import base64
import datetime

from Crypto.Cipher                     import PKCS1_OAEP
from Crypto.PublicKey                  import RSA
from src.system.logging.magic          import logger
from src.system.loading.config         import getConfig

TIME_WINDOW = 60

commands = [
    "showUsers",
    "showSSL",
    "showConfig",
    "showSystemStatus",
    "showRegion",
    "showHotFixRes"
]

commands = [
    "showUsers",
    "showSSL",
    "showConfig",
    "showSystemStatus",
    "showRegion",
    "showHotFixRes",
]

def signKeyVerify(sign, command) -> bool:
    if getConfig()['Security']['is_sign']:
        try:
            with open('data/api/private.key', 'r', encoding="UTF-8") as file:
                private_key = file.read()

            # encrypt
            system_sign = getConfig()['Security']['sign_key']
            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
            encrypted_message_bytes = base64.b64decode(sign)
            decrypted_message = cipher_rsa.decrypt(encrypted_message_bytes).decode()
            logger.info(f"Encrypt result: {decrypted_message}, origin: {sign}")

            request_message = decrypted_message.split('&')

            sign_status = time_status = cmd_status = False
            
            local_time_stamp = int(datetime.datetime.now().timestamp())
            
            # verify
            for msg in request_message:
                # sign match
                if "sign" in msg:
                    request_sign = msg.replace('sign=', '')
                    if request_sign == system_sign:
                        sign_status = True
                    else:
                        logger.error(f"Sign verify failed: system sign: {system_sign}, but request sign: {request_sign}")
                        sign_status = False
                    
                # time stamp match with window
                elif "time" in msg:
                    request_time_stamp = int(msg.replace('time=', ''))
                    time_difference = abs(local_time_stamp - request_time_stamp)
                    # 300s
                    if time_difference <= TIME_WINDOW:
                        time_status = True
                    else:
                        logger.error(f"Time stamp verify failed: system time stamp: {local_time_stamp}, but request time stamp: {request_time_stamp}. Difference: {time_difference} seconds")
                        time_status = False

                # command match
                elif "cmd" in msg:
                    cmd = msg.replace('cmd=', '')
                    if cmd == command:
                        cmd_status = True
                    else:
                        logger.error(f"Cmd verify failed: system cmd: {command}, but request cmd: {cmd}")
                        cmd_status = False

            # finally
            if sign_status and time_status and cmd_status:
                return True
            else:
                return False

        except Exception as err:
            logger.error(f"Encrypt error: {err}")
            return False
    else:
        logger.warning("Verify are disable, skip sign check")
        return True
