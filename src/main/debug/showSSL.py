try:
    from __main__ import app
except:
    from main import app

from src.system.logging.magic       import logger
from src.system.response.jsonMsg    import returnJsonMsg

import src.system.response.retcode  as path

@app.route('/develop/showSSL/server.<type>', methods = ['GET'])
def showSSLConfig(type):
    try:

        if type == "key":
            with open(path.SSL_KEY_PATH, "r", encoding="UTF-8") as file:
                data = file.read().replace('\n',"")
                file.close()
                
                logger.info(f"Try to view ssl key config succ: {data}")
                return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)

        elif type == "pem":
            with open(path.SSL_PEM_PATH, "r", encoding="UTF-8") as file:
                data = file.read().replace('\n',"")
                file.close()

                logger.info(f"Try to view ssl pem config succ: {data}")
                return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)
        
        else:
            logger.warning(f"Try to view ssl key config fail: Not found type: {type}")
            return returnJsonMsg(path.RESPONSE_FAIL, "Error", f"Not found type:{type}")

    except Exception as err:
        logger.error(f"Try to view ssl config fail: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
