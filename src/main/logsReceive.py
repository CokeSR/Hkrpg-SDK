from __main__                       import app
from flask                          import request
from src.system.logging.systemctl   import logger
from src.system.response.jsonMsg    import returnJsonMsg

import src.system.response.retcode as retcode

@app.route("/adsdk/dataUpload", methods = ['POST'])
@app.route("/apm/dataUpload", methods = ['POST'])
@app.route("/sdk/dataUpload", methods = ['POST'])
@app.route("/sophon/dataUpload", methods = ['POST'])
def getLog():
    logger.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    return {"code": 0, "message": "OK"}


# topic=plat_apm_sdk
@app.route("/common/h5log/log/batch", methods = ['POST'])
def h5logBatch():
    return returnJsonMsg(retcode.RESPONSE_SUCC, "success", "")
