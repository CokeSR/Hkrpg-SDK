from __main__                       import app
from flask                          import request
from src.system.logging.route       import logger       as userlog
from src.system.logging.systemctl   import logger       as syslog
from src.system.response.jsonMsg    import returnJsonMsg

import src.system.response.retcode as code

# 账号登出 
@app.route('/account/ma-cn-session/app/logout', methods = ['POST'])
def userLogout():
    uid = request.json['aid']
    token = request.json['token']['token']
    
    syslog.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    userlog.info(f"User's uid: {uid} logout succ, token:{token}")

    return returnJsonMsg(code.RESPONSE_SUCC, "OK","")
