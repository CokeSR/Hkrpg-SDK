import os
import sys
import base64
import time
import yaml
import src.system.response.retcode as rep

from flask                          import Flask
from src.system.logging.route       import logger as routelog
from src.system.logging.magic       import logger as magiclog
from src.system.logging.query       import logger as querylog
from src.system.logging.systemctl   import logger as syslog
from src.system.loading.config      import getConfig
from src.system.rebuild.config      import configRebuild
from src.system.check.emailStatus   import checkEmailConn
from src.system.check.regionConn    import checkRegionConn
from src.system.check.databaseConn  import checkMysqlConn
from src.system.check.configStatus  import check_config, checkRegion
from src.system.check.hotFixStatus  import checkHotFixRes


app = Flask(__name__,
    template_folder="data/static/templates/", 
    static_folder="data/static/",
)
app.secret_key = base64.b64encode(os.urandom(24))

# system loading
try:
    from src.main                           import *
    from src.main.debug                     import *
    from src.system.response.errorHander    import *
except ImportError as err:
    syslog.error(f"System error: {err}")
    sys.exit(0)

# protoful loading
try:
    from src.proto.latest                   import *
    from src.proto.prod_2_4_0           import *
except ImportError as err:
    syslog.error(f"System error: {err}")
    sys.exit(0)

# Check config exists
try:
    with open(rep.CONFIG_PATH, "r", encoding="utf-8") as file:
        try:
            config = yaml.safe_load(file)
            pass
        except Exception as err:
            syslog.error(err)
except FileNotFoundError:
    syslog.error(f"{'=' * 15} No such file or dictionary: {rep.CONFIG_PATH} {'=' * 15}")
    syslog.info(f"Auto build latest config... {configRebuild()}")
    sys.exit(0)

# Check services action
servicesCheckDict = {
    check_config: "CHECK CONFIG SETTINGS FAILED",
    checkMysqlConn: "CHECK DATABASE STATUS FAILED",
    checkEmailConn: "CHECK EMAIL SERVICE FAILED",
    checkRegion: "CHECK DISPATCH REGION FAILED",
    checkRegionConn: "CHECK REGION CONNECT FAILED",
    checkHotFixRes: "CHECK HOTFIX RESOURCE FAILED",
}

for checkFunc, errMsg in servicesCheckDict.items():
    if not checkFunc():
        syslog.error(f"{'=' * 15} {errMsg} {'=' * 15}")
        sys.exit(0)

# Optput service latest launch time in log files
logType = [routelog, magiclog, querylog, syslog]
for log in logType:
    log.info(
        f"{log} Latest launch time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
    )

if __name__ == "__main__":
    try:
        settings = getConfig()['App']
        syslog.info(f"SSL mode: {settings['ssl']}")
        syslog.info(f"{'=' * 15} CHECK SERVICE SETTINGS SUCC {'=' * 15}")

        if settings['ssl']:
            syslog.info(f"Hkrpg-sdkserver running at https://{settings['host']}:{settings['port']}")
            app.run(
                host = settings['host'],
                port = settings['port'],
                debug = settings['debug'],
                use_reloader = settings['reload'],
                threaded = settings['threaded'],
                ssl_context = (rep.SSL_PEM_PATH, rep.SSL_KEY_PATH)
            )
        else:
            syslog.info(f"Hkrpg-sdkserver running at http://{settings['host']}:{settings['port']}")
            app.run(
                host = settings['host'],
                port = settings['port'],
                debug = settings['debug'],
                use_reloader = settings['reload'],
                threaded = settings['threaded'],
            )

    except Exception as err:
        syslog.error(f"Starting service fail：{err}")
