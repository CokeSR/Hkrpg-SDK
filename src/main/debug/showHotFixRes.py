try:
    from __main__ import app
except:
    from main import app

from flask                             import request
from src.system.logging.magic          import logger
from src.system.response.jsonMsg       import returnJsonMsg
from src.system.response.requestVerify import signKeyVerify

import json
import src.system.response.retcode      as path


@app.route('/develop/showHotfixRes', methods = ['GET'])
def showHotFilxRes():
    try:
        cmd = "showHotfixRes"
        sign = request.args.get('sign')
        user = request.remote_addr
        logger.info(f"User: {user} get /develop/showHotfixRes/")
        if sign:
            signed = sign.replace(' ', '+')
            if signKeyVerify(signed, cmd):

                with open(path.HOTFIX_RES_PATH, '+r', encoding="UTF-8") as file:
                    data = json.loads(file.read())
                    logger.info(f"User: {user} try to load hot fix resource succ: {data}")
                    return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)
            else:
                msg = "sign key verify failed"
                logger.info(f"User: {user} load hot fix resource failed: {msg}")
                return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)
        else:
            msg = "sign key not found"
            logger.info(f"User: {user} load hot fix resource failed: {msg}")
            return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

    except Exception as err:
        logger.error(f"User: {user} load hot fix resource failed: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
