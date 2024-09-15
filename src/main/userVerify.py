from __main__                       import app
from flask                          import request
from time                           import time as epoch
from datetime                       import datetime
from src.system.logging.route       import logger       as userlog
from src.system.logging.systemctl   import logger       as syslog
from src.system.loading.database    import get_db
from src.system.loading.config      import getConfig
from src.system.response.msgSafe    import mask_email, mask_string
from src.system.response.requestGet import request_ip
from src.system.response.jsonMsg    import returnJsonMsg

import json
import pymysql
import random
import src.system.response.retcode as retcode

# 登录二检
@app.route('/hkrpg_cn/combo/granter/login/v2/login', methods = ['POST'])
@app.route('/hkrpg_global/combo/granter/login/v2/login', methods = ['POST'])
def accountLoginV2() -> str:
    timestamp = int(datetime.now().timestamp())
    config = getConfig()['Client']

    userlog.info(f"V2 login timestamp (service time): {timestamp}")
    syslog.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")

    try:
        data = json.loads(request.json["data"])
        cursor = get_db().cursor(pymysql.cursors.DictCursor)

        token_query = ("SELECT * FROM `t_accounts_tokens` WHERE `token` = %s AND `uid` = %s")
        cursor.execute(token_query, (data["token"], data["uid"]))
        user_tokens = cursor.fetchone()

        if not user_tokens:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "游戏账号信息缓存错误", "")

        # token 5 天有效期
        tokenCreateTime = int(user_tokens["epoch_generated"])
        tokenExpirationTime = tokenCreateTime + 432000

        if tokenExpirationTime < timestamp:
            userlog.error(f"The UID {data['uid']} login token create time: {user_tokens['epoch_generated']}. But expiration time is {tokenExpirationTime}, must be relogin.")

            # 清除过期token
            deleteExpirationToken = "DELETE FROM `t_accounts_tokens` WHERE %s"
            cursor.execute(deleteExpirationToken, user_tokens["epoch_generated"])

            userlog.error(f"User's uid:{user_tokens['uid']} login Failed. Token is expiration.")
            userlog.error(f"Delete expiration token:{user_tokens['token']}, User's uid:{user_tokens['uid']}")
            return returnJsonMsg(retcode.RESPONSE_FAIL, "账号Token过期，请点击右上角重新登录", "")

        # 用户检查
        user_query = "SELECT * FROM `t_accounts` WHERE `uid` = %s AND `type` = %s"
        cursor.execute(user_query, (user_tokens["uid"], retcode.ACCOUNT_TYPE_NORMAL))
        user = cursor.fetchone()

        if not user:
            userlog.info(f"User's uid:{user_tokens['uid']} login Failed. User not found")
            return returnJsonMsg(retcode.RESPONSE_FAIL, "未找到用户", "")

        # 写入 comboToken
        ip = request_ip(request)
        epoch_generated = int(epoch())
        device = request.json["device"]
        combo_token = "".join(random.choices("0123456789abcdef", k=40))

        combo_token_query = "INSERT INTO `t_combo_tokens` (`uid`, `token`, `device`, `ip`, `epoch_generated`) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `token` = VALUES(`token`), `device` = VALUES(`device`), `ip` = VALUES(`ip`), `epoch_generated` = VALUES(`epoch_generated`)"
        cursor.execute(combo_token_query, (user["uid"], combo_token, device, ip, epoch_generated))

        data = {
            "combo_id": 0,
            "open_id": user["uid"],
            "combo_token": combo_token,
            "data": {
                "guest": config['guest']
            },
            "heartbeat": config['heartbeat'],
            "account_type": 1,
            "fatigue_remind": None,
        }

        userlog.info(f"User's uid:{user_tokens['uid']} login successful, combo_token:{combo_token}")
        return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", data)
    except Exception as err:
        userlog.error(f"Systemctl error: {err}")
        return returnJsonMsg(retcode.RESPONSE_FAIL, "系统错误，请联系管理员", "")


# Token 登录检查
@app.route("/hkrpg_cn/mdk/shield/api/verify", methods=["POST"])
@app.route("/hkrpg_global/mdk/shield/api/verify", methods=["POST"])
def accountVerify():
    config = getConfig()['Api']
    syslog.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")

    try:
        uid = request.json['uid']
        token = request.json['token']
        
        # 查库对比
        cursor = get_db().cursor(pymysql.cursors.DictCursor)
        query_token = "SELECT token FROM `t_accounts_tokens` WHERE `uid` = %s"
        cursor.execute(query_token, uid)
        user_tokens = cursor.fetchone()
        
        userlog.info(f"Get uid:{uid}, token:{token} prepare for the check")
        
        # Token 是否存在
        if not user_tokens:
            userlog.warning(f"User's uid {uid} shield api verify failed. Token not found")
            return returnJsonMsg(retcode.RESPONSE_FAIL, "游戏账号信息缓存错误", "")
        
        # Token 对称
        if user_tokens['token'] == token:
            # 获取用户信息
            query_user = "SELECT * FROM `t_accounts` WHERE `uid` = %s"
            cursor.execute(query_user, uid)
            users = cursor.fetchone()
            
            content = {
                "account": {
                    "uid": uid,
                    "name": mask_string(users["name"]),
                    "mobile": mask_string(users["mobile"]),
                    "email": mask_email(users["email"]),
                    "is_email_verify": "1",
                    "realname": "**游",
                    "identity_card": "123************456",
                    "token": token,
                    "safe_mobile": "",
                    "facebook_name": "",
                    "google_name": "",
                    "twitter_name": "",
                    "game_center_name": "",
                    "apple_name": "",
                    "sony_name": "",
                    "tap_name": "",
                    "country": "",
                    "reactivate_ticket": "",
                    "area_code": "",
                    "device_grant_ticket": "",
                    "steam_name": "",
                    "unmasked_email": "",
                    "unmasked_email_type": 0,
                    "cx_name": "",
                },
                "device_grant_required": config['device_grant_required'],
                "safe_moblie_required": config['safe_moblie_required'],
                "realperson_required": config['realperson_required'],
                "reactivate_required": config['reactivate_required'],
                "realname_operation": None
            }
            
            userlog.info(f"User's uid {uid} shield api verify succ.")
            return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
        else:
            userlog.warning(f"User's uid {uid} shield api verify failed.")
            return returnJsonMsg(retcode.RESPONSE_FAIL, "游戏账号信息缓存错误", "")

    except Exception as err:
        userlog.error(f"Systemctl error: {err}")
        return returnJsonMsg(retcode.RESPONSE_FAIL, "系统错误，请联系管理员", "")
