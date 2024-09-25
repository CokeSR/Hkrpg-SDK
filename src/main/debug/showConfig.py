try:
    from __main__ import app
except:
    from main import app

from flask                             import request
from src.system.loading.config         import getConfig
from src.system.logging.magic          import logger
from src.system.response.jsonMsg       import returnJsonMsg
from src.system.response.requestVerify import signKeyVerify
import src.system.response.retcode     as path

@app.route('/develop/showConfig', methods = ['GET'])
def showConfig():
    try:
        cmd = "showConfig"
        sign = request.args.get('sign')
        user = request.remote_addr
        logger.info(f"User: {user} try to get /develop/showConfig/")
        if sign:
            signed = sign.replace(' ', '+')

            if signKeyVerify(signed, cmd):
                data = getConfig()
                logger.info(f"User: {user} view system config succ: {data}")
                return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)

            else:
                msg = "sign key verify failed"
                logger.error(f"User: {user} view system config failed: {msg}")
                return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

        else:
            msg = "sign key not found"
            logger.error(f"User: {user} view system config failed: {msg}")
            return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

    except Exception as err:
        logger.error(f"User: {user} view system config failed: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
