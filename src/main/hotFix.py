from __main__                   import app
from flask                      import Response, request
from base64                     import b64encode
from urllib.parse               import urlencode
from src.system.logging.query   import logger

import json
import src.proto.latest.Gateserver_pb2 as latestQueryGateway
import src.system.response.retcode     as path

# 热更新 PATCH
# ?version=CNPRODWin2.4.0&t=1725164968&uid=100432316&language_type=1&platform_type=3&dispatch_seed=5e645c358d&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=300086382
@app.route("/query_gateway", methods=["GET"])
def query_gateway() -> str:
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        time            =   request.args.get("t")
        uid             =   request.args.get("uid")
        version         =   request.args.get("version")
        language_type   =   request.args.get("language_type")
        platform_type   =   request.args.get("platform_type")
        dispatchSeed    =   request.args.get("dispatch_seed")
        channel_id      =   request.args.get("channel_id")
        sub_channel_id  =   request.args.get("sub_channel_id")
        is_need_url     =   request.args.get("is_need_url")
        account_type    =   request.args.get("account_type")
        account_uid     =   request.args.get("account_uid")
        if (
            version
            and time
            and uid
            and language_type
            and platform_type
            and dispatchSeed
            and channel_id
            and sub_channel_id
            and is_need_url
            and account_type
            and account_uid
        ):
            """
            @Official
            response.ip = "47.100.186.169"
            response.port = 23301
            """
            # 截取版号
            def getClientVersion(version):
                client = ["Win", "Android", "iOS"]
                for type in client:
                    if type in version:
                        hotFixVer = version.split(type)[1]
                return hotFixVer

            # 根据版号获得热更信息 意外版本不进行阻塞 直接返回 region_not_match
            with open(path.HOTFIX_RES_PATH, '+r', encoding="UTF-8") as file:
                res = json.loads(file.read())
                try:
                    ver = getClientVersion(version)
                    rescurseData = res[ver]
                    logger.info(f"Load hotFix version config succ: {ver}, res: {rescurseData}")
                except Exception:
                    logger.warning(f"Not found hotFix version config: {ver}")

            # 旧版本检查 后续添加
            if ver == "2.4.0":
                logger.warning(f"Query {ver} client hotfix, not latest version")

                import src.proto.prod_2_4_0.Gateserver_2_4_0_pb2 as oldQueryGateway
                response = oldQueryGateway.Gateserver_2_4_0()
            else:
                response = latestQueryGateway.Gateserver()

            response.region_name        =  "prod_cokesr"
            response.ip                 =  "127.0.0.1"
            response.port               =  1234
            response.msg                =  "游戏正在维护中，详情请注意官方公告"
            response.lua_url            =  str(rescurseData['lua_url'])
            response.ifix_url           =  str(rescurseData['ifix_url'])
            response.ex_resource_url    =  str(rescurseData['ex_resource_url'])
            response.asset_bundle_url   =  str(rescurseData['asset_bundle_url'])
            response.ifix_version       =  str(rescurseData['ifix_version'])
            response.mdk_res_version    =  str(rescurseData['mdk_res_version'])
            response.client_secret_key  =  str(rescurseData['client_secret_key'])

            response.enable_version_update                      = True
            response.enable_design_data_bundle_version_update   = True
            response.event_tracking_open                        = True
            response.enable_android_middle_package              = True
            response.network_diagnostic                         = True
            """
            beta, useless on release 
            response.enable_watermark = True
            response.close_redeem_code = True
            """
            data = response.SerializeToString()
            base64_str = b64encode(data).decode()
            return base64_str
        else:
            return Response("5Y+C5pWw6ZSZ6K+v", content_type="text/plain")
    except Exception as err:
        # region_not_match
        logger.error(f"Failed to return msg: {err}")
        base64_str = "GAM6GGNsaWVudCB2ZXJzaW9uIG5vdCBtYXRjaFIKcHJvZF9nZl9jbvoXNua4uOaIj+ato+WcqOe7tOaKpOS4re+8jOivpuaDheivt+WFs+azqOWumOaWueWFrOWRiuOAgg=="
        return base64_str
