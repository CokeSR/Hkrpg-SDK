from __main__ import app
import re
import random
import string
import src.system.response.retcode as code

from pytz                           import timezone
from time                           import time as epoch
from datetime                       import datetime, timedelta
from src.system.logging.systemctl   import logger
from src.system.decrypt.password    import password_hash
from src.system.loading.database    import get_db
from src.system.loading.config      import getConfig
from src.system.response.jsonMsg    import returnJsonMsg
from src.system.response.sendCode   import send_email_smtp

from flask import (
    flash,
    render_template, 
    request, 
    session,
)

utz = timezone('UTC')
ctz = timezone('Asia/Shanghai')

@app.route('/account/register', methods = ['GET','POST'])
def accountRegister():
    session.permanent = True
    cursor = get_db().cursor()
    
    if request.method == 'POST':
        username = request.form.get("username")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        verifycode = request.form.get("verifycode")
        password = request.form.get("password")
        passwordv2 = request.form.get("passwordv2")
        
        cursor.execute("SELECT * FROM `t_accounts` WHERE `mobile` = %s or `email` = %s", (mobile, email,))
        account_status = cursor.fetchone()
        
        logger.info(f"User '{email}' try to register account.")
        
        if account_status:
            flash("账号已被注册，请重试手机号或邮箱", "error")
            logger.info(f"User '{email}' register account failed: Already exists.")
            return render_template("accountRegister.tmpl", config = getConfig())
        
        if not re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email):
            flash("邮箱格式不正确", "error")
            return render_template("accountRegister.tmpl", config = getConfig())
        
        if not re.fullmatch(r"^\d{11}$", mobile):
            flash("手机号码格式不正确", "error")
            return render_template("accountRegister.tmpl", config = getConfig())
        
        if getConfig()["Mail"]["enable"] and "register_codes" in session:
            valid = False
            for register_code_info in session["register_codes"]:
                if (
                    register_code_info["email"] == email
                    and register_code_info["verification_code"] == verifycode
                    and register_code_info["valid"]
                    and register_code_info["timeout"] >= datetime.now(utz)
               ):
                    valid = True
                    break
            
            if not valid:
                flash("验证码错误或失效", "error")
                logger.info(f"User '{email}' register account failed: The verification code is invalid.")
                return render_template("accountRegister.tmpl", config = getConfig())
        
        if password != passwordv2:
            flash("两次输入的密码不一致", "error")
            logger.info(f"User '{email}' register account failed: The password is invalid")
            return render_template("accountRegister.tmpl", config = getConfig())
        
        if len(password) < getConfig()["Security"]["min_password_len"]:
            flash(f"密码长度不能小于 {getConfig()['Security']['min_password_len']} 字节", "error")
            return render_template("accountRegister.tmpl", config = getConfig())

        cursor.execute(
            "INSERT INTO `t_accounts` (`name`, `mobile`, `email`, `password`, `type`, `epoch_created`) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                username,
                mobile,
                email,
                password_hash(password),
                code.ACCOUNT_TYPE_NORMAL,
                int(epoch()),
            ),
        )
        
        logger.info(f"User '{email}' register account SUCC.")
        
        flash("游戏账号注册成功，请返回登录", "success")
    return render_template("accountRegister.tmpl", config = getConfig())


# 邮件验证码 用于注册
@app.route("/account/register_code", methods=['POST'])
def register_code():
    session.permanent = True
    email = request.form.get("email")
    email_pattern = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(email_pattern, email):
        return returnJsonMsg(code.RESPONSE_FAIL, "邮箱格式不正确", {})

    cursor = get_db().cursor()
    user_query = "SELECT * FROM `t_accounts` WHERE `email` = %s"
    cursor.execute(user_query, (email,))
    user = cursor.fetchone()

    if user:
        return returnJsonMsg(code.RESPONSE_FAIL, "邮箱已经被注册了", {})

    if "register_codes" in session:
        session["register_codes"] = [code for code in session["register_codes"] if code["timeout"] >= datetime.now(utz)]
        
        if len(session["register_codes"]) > 5:
            except_time = session["register_codes"][-6]["timeout"].astimezone(ctz).strftime("%Y-%m-%d %H:%M:%S")
            return returnJsonMsg(code.RESPONSE_FAIL, f"发送验证码频率超过限制，请在{except_time}后再试", {})

    if "send_code_timeout" in session and session["send_code_timeout"] > datetime.now(utz):
        except_time = session["send_code_timeout"].astimezone(ctz).strftime("%Y-%m-%d %H:%M:%S")
        return returnJsonMsg(code.RESPONSE_FAIL, f"发送验证码间隔为60秒，请在{except_time}后再试", {})

    verification_code = "".join(random.choices(string.digits, k=getConfig()['Security']['verify_code_length']))

    logger.info(f"The user {email} verification code: {verification_code}")

    if not send_email_smtp(verification_code, email):
        return returnJsonMsg(code.RESPONSE_FAIL, "发送邮件失败，请联系管理员", {})

    new_register_code_info = {
        "email": email,
        "verification_code": verification_code,
        "timeout": datetime.now(utz) + timedelta(seconds=300),
        "valid": True,
    }

    if "register_codes" in session:
        for register_code_info in session["register_codes"]:
            if register_code_info["email"] == email:
                register_code_info["valid"] = False
        session["register_codes"].append(new_register_code_info)
    else:
        session["register_codes"] = [new_register_code_info]

    session["send_code_timeout"] = datetime.now(utz) + timedelta(seconds=60)
    return returnJsonMsg(code.RESPONSE_SUCC, "验证码发送成功，请查收邮箱", {})
