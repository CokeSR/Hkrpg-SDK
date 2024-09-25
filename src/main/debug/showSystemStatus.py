try:
    from __main__ import app
except:
    from main import app

from flask                             import request
from src.system.logging.magic          import logger
from src.system.response.jsonMsg       import returnJsonMsg
from src.system.response.requestVerify import signKeyVerify

import time
import psutil
import src.system.response.retcode     as path

@app.route('/develop/showSystemStatus', methods = ['GET'])
def showSystemStatus():
    try:
        cmd = "showSystemStatus"
        sign = request.args.get('sign')
        user = request.remote_addr
        logger.info(f"User: {user} try to get /develop/showSystemStatus/")

        time_stamp          = int(time.time())                   # 系统时间戳
        cpu_count           = psutil.cpu_count(logical=True)     # CPU逻辑核心数
        cpu_percent         = psutil.cpu_percent(interval=1)     # CPU的使用率
        total_memory        = psutil.virtual_memory().total      # 物理内存总量
        cpu_count_physical  = psutil.cpu_count(logical=False)    # CPU物理核心数
        available_memory    = psutil.virtual_memory().available  # 可用内存总量
        memory_percent      = psutil.virtual_memory().percent    # 内存使用率
        disk_partitions     = psutil.disk_partitions()           # 磁盘分区
        net_if_addrs        = psutil.net_if_addrs()              # 网卡IP地址信息

        if sign:
            signed = sign.replace(' ', '+')
            if signKeyVerify(signed, cmd):
                data = {
                    "time": time_stamp,
                    "cpu": {
                        "count": cpu_count,
                        "pjysical_count": cpu_count_physical,
                        "current_percent": cpu_percent,
                    },
                    "memory": {
                        "total_memory(GB)": total_memory  / 10 ** 9,
                        "available_memory(GB)": available_memory / 10 ** 9,
                        "use_percent(%)": memory_percent,
                    },
                    "disk": {
                        "region": disk_partitions,
                    },
                    "network": {
                        "ip_address": net_if_addrs,
                    },
                }
                logger.info(f"User: {user} get system status succ: {data}")
                return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)

            else:
                msg = "sign key verify failed"
                logger.error(f"User: {user} get system status failed: {msg}")
                return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

        else:
            msg = "sign key not found"
            logger.error(f"User: {user} get system status failed: {msg}")
            return returnJsonMsg(path.RESPONSE_FAIL, "Error", msg)

    except Exception as err:
        logger.error(f"User: {user} get system status failed: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
