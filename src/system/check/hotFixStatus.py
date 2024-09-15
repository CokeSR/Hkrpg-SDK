import re
import json
import src.system.response.retcode    as path

from src.system.logging.systemctl     import logger

def checkHotFixRes() -> bool:
    try:
        with open(path.HOTFIX_RES_PATH, '+r', encoding="UTF-8") as file:
            data = json.loads(file.read())
            
            # loadVersions = []
            for version, resource in data.items():
                # loadVersions.append(version)
                # 版本检
                if version == "":
                    logger.error(f"Not found hotFix version config")
                    return False
                
                if not re.search(r'^[0-9]\.[0-9]\.[0-9]$', version):
                    logger.error(f"Unknown version config: {version}")
                    return False

                logger.info(f"Load hotFix version: {version}, resource: {resource}")

                # 参检
                for url, content in resource.items():
                    logger.info(f"Get hotFix details: {url}:{content}")

                if (
                    "lua_url"          not in resource or 
                    "ifix_url"         not in resource or 
                    "ex_resource_url"  not in resource or
                    "asset_bundle_url" not in resource or
                    "ifix_version"     not in resource or
                    "mdk_res_version"  not in resource
                    ):
                    logger.error(f"Load {version} hotFix resource fail: An item is missing")
                    return False
                else:
                    logger.info(f"Load {version} hotFix resource succ.")

            """
            # 与第 12 行、第 14 行关联
            # json.loads() 会过滤掉重复的键 | 防呆不防傻，真的会有天才填重复的版本号吗
            sameVersion = set(loadVersions)
            for ver in sameVersion:
                if loadVersions.count(ver) > 1:
                    logger.error(f"The same version exists: {ver}")
                    return False
            """

    except Exception as err:
        if "Expecting value" in str(err):
            logger.error(f"Try to load hotFix resource file failed: {err}, please check JSON grammar.")
            return False
        else:
            logger.error(f"Try to load hotFix resource file failed: {err}")
            return False

    logger.info(f"{'=' * 15} LOADING HOTFIX RESOURCE SUCC {'=' * 15}")
    return True
