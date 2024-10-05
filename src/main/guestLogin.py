from __main__                       import app
from flask                          import request
from time                           import time         as epoch
from src.system.logging.route       import logger       as userlog
from src.system.logging.systemctl   import logger       as syslog
from src.system.loading.config      import getConfig
from src.system.loading.database    import get_db
from src.system.response.jsonMsg    import returnJsonMsg

import random
import string
import pymysql
import src.system.response.retcode as code


@app.route('/hkrpg_cn/mdk/guest/guest/v2/login', methods = ['POST'])
@app.route('/hkrpg_global/mdk/guest/guest/v2/login', methods = ['POST'])
def guestLogin():
    syslog.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    cursor = get_db().cursor(pymysql.cursors.DictCursor)
    config = getConfig()['Client']
    if config['guest']:
        try:
            device = request.json['device']
            client = request.json['client']
            ver    = request.json['g_version']

            # 访客检查
            userlog.info(f"Guest '{device}' try to login, client_type: {client}, game_version: {ver}")
            user_name = f"游客-{device[0:10]}"
            guest_query = "SELECT * FROM `t_accounts_guests` WHERE `device` = %s"
            cursor.execute(guest_query, device)
            guest_msg = cursor.fetchone()

            guest_query = "SELECT * FROM `t_accounts` WHERE `name` = %s and `type` = 0"
            cursor.execute(guest_query, user_name)
            user = cursor.fetchone()

            if not guest_msg:
                # 注册
                if not user:
                    cursor.execute(
                        "INSERT INTO `t_accounts` (`name`, `mobile`, `email`, `password`, `type`, `epoch_created`) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            user_name,
                            "",
                            "",
                            "",
                            code.ACCOUNT_TYPE_GUEST,
                            int(epoch()),
                        ),
                    )
                    userlog.info(f"Guest '{device}' register account SUCC")

                # token 下发
                latest_token = "".join(random.choices(string.ascii_letters, k=40))
                guest_reg = "INSERT INTO `t_accounts_guests` (`device`,`client`,`version`,`token`,`epoch_generated`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(guest_reg, (device, client, ver, latest_token, int(epoch())))
                userlog.info(f"Guest '{device}' content update SUCC")

            data = {
                "account_type": str(user['type']),
                "guest_id": str(user['uid']),
            }

            return returnJsonMsg(code.GUEST_LOGIN_SUCC, "OK", data)
        except Exception as err:
            userlog.error(f"System error: {err}")
            return returnJsonMsg(code.GUEST_LOGIN_FAIL, "系统错误, 请联系管理员", "")
    else:
        userlog.info(f"Guest '{device}' try to login failed: function disabled")
        return returnJsonMsg(code.GUEST_LOGIN_FAIL,"游客登录已关闭", "")
