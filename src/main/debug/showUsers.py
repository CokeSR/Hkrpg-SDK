try:
    from __main__ import app
except:
    from main import app

from src.system.loading.database    import get_db
from src.system.logging.magic       import logger
from src.system.response.jsonMsg    import returnJsonMsg

import src.system.response.retcode  as path

@app.route('/develop/showUsers', methods = ['GET'])
def showAccountUsers():
    try:
        query = get_db().cursor()
        query.execute("SELECT * FROM `t_accounts`")
        data = query.fetchall()
        logger.info(f"Try to query account message succ: {data}")

        return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)
    except Exception as err:
        logger.error(f"Try to query account message fail: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
