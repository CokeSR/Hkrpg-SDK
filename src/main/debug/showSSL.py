try:
    from __main__ import app
except:
    from main import app

from flask                             import request
from src.system.logging.magic          import logger
from src.system.response.jsonMsg       import returnJsonMsg
from src.system.response.requestVerify import signKeyVerify

import src.system.response.retcode     as path

@app.route('/develop/showSSL/server.<type>', methods = ['GET'])
def showSSLConfig(type):
    try:
        cmd = "showSSL"
        sign = request.args.get('sign')
        user = request.remote_addr
        logger.info(f"User: {user} try to get /develop/showSSL/")
        if sign:
            signed = sign.replace(' ', '+')
            if signKeyVerify(signed, cmd):
                if type == "key":
                    with open(path.SSL_KEY_PATH, "r", encoding="UTF-8") as file:
                        data = file.read().replace('\n',"")
                        file.close()
                        logger.info(f"User: {user} view ssl key config succ: {data}")
                        return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)
                elif type == "pem":
                    with open(path.SSL_PEM_PATH, "r", encoding="UTF-8") as file:
                        data = file.read().replace('\n',"")
                        file.close()
                        logger.info(f"User: {user} view ssl pem config succ: {data}")
                        return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)
                else:
                    msg = f"Not found type: {type}"
                    logger.error(f"User: {user} view ssl key config failed: {msg}")
                    return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

            else:
                msg = "sign key verify failed"
                logger.error(f"User: {user} view ssl key config failed: {msg}")
                return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)
    
        else:
            msg = "sign key not found"
            logger.error(f"User: {user} view ssl key config failed: {msg}")
            return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)  

    except Exception as err:
        logger.error(f"User: {user} view ssl config failed: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
