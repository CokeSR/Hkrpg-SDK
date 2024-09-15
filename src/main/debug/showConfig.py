try:
    from __main__ import app
except:
    from main import app

from src.system.loading.config      import getConfig
from src.system.logging.magic       import logger
from src.system.response.jsonMsg    import returnJsonMsg

import src.system.response.retcode as path

@app.route('/develop/showConfig', methods = ['GET'])
def showConfig():
    try:

        data = getConfig()
        logger.info(f"Try to view system config succ: {data}")
        return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)

    except Exception as err:
        logger.info(f"Try to view system config fail: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))

