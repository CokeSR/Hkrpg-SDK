import requests

from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig

def checkRegionConn() -> bool:
    regionCofig = getConfig()['Region']
    
    for region in regionCofig:
        title       = region['title']
        dispatchUrl = region['dispatchUrl']
        
        try:
            status = requests.get(dispatchUrl, timeout = 5)

            if status.status_code == 200:
                logger.info(f"Title: {title}, dispatchUrl: {dispatchUrl} Try connect successful. Return msg: {status.text}")

        except Exception as err:
            # 如果是本地热更新，忽略这个错误
            if "127.0.0.1" in dispatchUrl or "localhost" in dispatchUrl:
                logger.warning(f"Title: {title}, dispatchUrl: {dispatchUrl} is a local address, skipping the connection check")
                continue

            logger.warning(f"Title: {title}, dispatchUrl: {dispatchUrl} Try connect failed")
    
    logger.info(f"{'=' * 15} CHECK DISPATCHURL CONNECT DONE {'=' * 15}")

    return True
