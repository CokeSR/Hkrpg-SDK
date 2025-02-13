try:
    from __main__ import app
except:
    from main import app

from flask                             import request
from src.system.loading.database       import get_db
from src.system.logging.magic          import logger
from src.system.response.jsonMsg       import returnJsonMsg
from src.system.response.requestVerify import signKeyVerify

import src.system.response.retcode     as path

@app.route('/develop/showUsers', methods = ['GET'])
def showAccountUsers():
    try:
        cmd = "showUsers"
        sign = request.args.get('sign')
        user = request.remote_addr
        logger.info(f"User: {user} try to get /develop/showUsers/")
        if sign:
            signed = sign.replace(' ', '+')
            if signKeyVerify(signed, cmd):
                query = get_db().cursor()
                query.execute("SELECT * FROM `t_accounts`")
                data = query.fetchall()
                logger.info(f"User: {user} query account message succ: {data}")
                return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)

            else:
                msg = "sign key verify failed"
                logger.error(f"User: {user} query account message failed: {msg}")
                return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)
    
        else:
            msg = "sign key not found"
            logger.error(f"User: {user} query account message failed: {msg}")
            return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

    except Exception as err:
        logger.error(f"User: {user} query account message failed: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
