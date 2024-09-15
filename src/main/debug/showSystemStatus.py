try:
    from __main__ import app
except:
    from main import app

from src.system.logging.magic       import logger
from src.system.response.jsonMsg    import returnJsonMsg

import psutil
import src.system.response.retcode  as path

@app.route('/develop/systemStatus', methods = ['GET'])
def showSystemStatus():
    try:
        cpu_count           = psutil.cpu_count(logical=True)     # CPU逻辑核心数
        cpu_percent         = psutil.cpu_percent(interval=1)     # CPU的使用率
        total_memory        = psutil.virtual_memory().total      # 物理内存总量
        cpu_count_physical  = psutil.cpu_count(logical=False)    # CPU物理核心数
        available_memory    = psutil.virtual_memory().available  # 可用内存总量
        memory_percent      = psutil.virtual_memory().percent    # 内存使用率
        disk_partitions     = psutil.disk_partitions()           # 磁盘分区
        net_if_addrs        = psutil.net_if_addrs()              # 网卡IP地址信息
        data = {
            "CPU": {
                "物理核心数": cpu_count_physical,
                "逻辑核心数": cpu_count,
                "当前使用率": cpu_percent,
            },
            "Memory": {
                "物理内存总量(GB)": total_memory  / 10 ** 9,
                "可用内存总量(GB)": available_memory / 10 ** 9,
                "内存使用率(%)": memory_percent,
            },
            "Disk": {
                "磁盘分区": disk_partitions,
            },
            "Network": {
                "网卡IP地址信息": net_if_addrs,
            },
        }
        logger.info(f"Try to get system status succ: {data}")
        return returnJsonMsg(path.RESPONSE_SUCC, "OK", data)
    except Exception as err:
        logger.info(f"Try to get system status fail: {err}")
        return returnJsonMsg(path.RESPONSE_FAIL, "Error", str(err))
