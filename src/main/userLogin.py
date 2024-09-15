from __main__                       import app
from flask                          import request
from time                           import time         as epoch
from src.system.logging.route       import logger       as userlog
from src.system.logging.systemctl   import logger       as syslog
from src.system.loading.config      import getConfig
from src.system.loading.database    import get_db
from src.system.response.jsonMsg    import returnJsonMsg
from src.system.response.requestGet import request_ip
from src.system.response.msgSafe    import mask_email, mask_string

import re
import random
import string
import pymysql
import src.system.response.retcode as code

def validate_user_format(user):
    phone_pattern = r"^\d{11}$"
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return (re.match(phone_pattern, user) is not None or re.match(email_pattern, user) is not None)


# 登录一检
@app.route('/hkrpg_cn/mdk/shield/api/login', methods = ['POST'])
@app.route('/hkrpg_global/mdk/shield/api/login', methods = ['POST'])
def accountLogin() -> str:
    config = getConfig()['Api']
    syslog.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    try:
        cursor = get_db().cursor(pymysql.cursors.DictCursor)
        
        # 传参正确
        if "account" not in request.json:
            return returnJsonMsg(code.RESPONSE_FAIL, "缺少登录凭据", "")
        
        # 国内登录正式化 不进行用户名登录 "OR `name` = %s"
        userName = request.json["account"]
        login_query = "SELECT * FROM `t_accounts` WHERE (`email` = %s OR `mobile` = %s) AND `type` = %s"
        cursor.execute(login_query, (userName, userName, code.ACCOUNT_TYPE_NORMAL))
        user = cursor.fetchone()
        
        # 登录弱检查
        if not validate_user_format(userName):
            userlog.warning(f"User {userName} login fail: format error")
            return returnJsonMsg(code.RESPONSE_FAIL, "错误的登录格式,仅可用手机号或邮箱进行登录", "")
        
        if not user:
            userlog.warning(f"User {userName} login fail: account not found")
            return returnJsonMsg(code.RESPONSE_FAIL, "该账号未注册", "")
        
        # token 登录检查
        def checkToken(uid):
            check_token = "SELECT token FROM `t_accounts_tokens` WHERE `uid` = %s"
            cursor.execute(check_token, uid)
            old_token = cursor.fetchone()

            # 如果没有 Token (首次登录)则签发并记录，否则用库里的
            if not old_token:
                device_id = request.headers.get("x-rpc-device_id")
                
                userlog.info(f"User {userName} Token not found, create it.")
                userlog.info(f"Request headers: {device_id}")
                
                ip = request_ip(request)
                epoch_generated = int(epoch())
                # 40 位令牌
                latest_token = "".join(random.choices(string.ascii_letters, k=40))
                
                insert_token_query = "INSERT INTO `t_accounts_tokens` (`uid`, `token`, `device`, `ip`, `epoch_generated`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_token_query, (user['uid'], latest_token, device_id, ip, epoch_generated))
                
                userlog.info(f"Try to get uid {uid} Token:{latest_token}, that's the latest token, create timestamp:{epoch_generated}")
                return latest_token
            else:
                token = old_token['token']
                userlog.info(f"Try to get uid {uid} Token:{token}, that's the origin token in service")
                return token

        token = checkToken(user['uid'])

        data = {
            "account": {
                "uid": str(user['uid']),
                "name": mask_string(user["name"]),
                "mobile": mask_string(user["mobile"]),
                "email": mask_email(user["email"]),
                "is_email_verify":"1",
                "realname":"**游",
                "identity_card":"123************456",
                "token": token,
                "safe_mobile":"",
                "facebook_name":"",
                "google_name":"",
                "twitter_name":"",
                "game_center_name":"",
                "apple_name":"",
                "sony_name":"",
                "tap_name":"",
                "country":"",
                "reactivate_ticket":"",
                "area_code":"",
                "device_grant_ticket":"",
                "steam_name":"",
                "unmasked_email":"",
                "unmasked_email_type":0,
                "cx_name":""
            },
            "device_grant_required": config['device_grant_required'],
            "safe_moblie_required": config['safe_moblie_required'],
            "realperson_required": config['realperson_required'],
            "reactivate_required": config['reactivate_required'],
            "realname_operation": None
        }
        userlog.info(f"User {userName} try to login. Token:{token}")
        return returnJsonMsg(code.RESPONSE_SUCC, "OK", data)
    except Exception as err:
        userlog.error(f"System error: {err}")
        return returnJsonMsg(code.RESPONSE_FAIL, "系统错误，请联系管理员", "")
