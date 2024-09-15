from __main__                       import app
from flask                          import request
from base64                         import b64encode
from urllib.parse                   import urlencode
from src.system.loading.config      import getConfig
from src.system.logging.query       import logger
from src.system.response.jsonMsg    import returnJsonMsg, returnJsonMsg_short

import src.proto.latest.DispatchRegionData_pb2 as queryDispatch

# Dispatch 区域登录
# version=CNPRODWin2.4.0&t=1725164968&language_type=1&platform_type=3&channel_id=1&sub_channel_id=1&is_new_format=1
@app.route('/query_dispatch', methods = ['GET'])
def queryRegion() -> str:
    """
    @Example:
        region_list {
        name: "prod_gf_cn"
        dispatch_url: "https://prod-gf-cn-dp01.bhsr.com/query_gateway"
        env_type: "0"
        display_name: "星穹列车"
        }
    """
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        t               =  request.args.get("t")
        version         =  request.args.get("version")
        language_type   =  request.args.get("language_type")
        platform_type   =  request.args.get("platform_type")
        channel_id      =  request.args.get("channel_id")
        sub_channel_id  =  request.args.get("sub_channel_id")
        is_new_format   =  request.args.get("is_new_format")
        if (
            version
            and t
            and language_type
            and platform_type
            and channel_id
            and sub_channel_id
            and is_new_format
        ):
            # 截取版号
            def getClientVersion(version):
                client = ["Win", "Android", "iOS"]
                for type in client:
                    if type in version:
                        hotFixVer = version.split(type)[1]
                return hotFixVer

            ver = getClientVersion(version)

            # 旧版本检查 后续添加
            if ver == "2.4.0":
                logger.warning(f"Query {ver} client dispatch, not latest version")
                
                import src.proto.prod_2_4_0.DispatchRegionData_2_4_0_pb2 as oldDispatchRegion
                response = oldDispatchRegion.DispatchRegionData_2_4_0()
                updateRegionList = oldDispatchRegion.DispatchRegionData_2_4_0()
            else:
                response = queryDispatch.DispatchRegionData()
                updateRegionList = queryDispatch.DispatchRegionData()

            dispatchList = getConfig()['Region']

            response.retcode = 0
            for info in dispatchList:
                region_info                 =    response.region_list.add()
                region_info.msg             =    "Hkrpg-CokeSR"
                region_info.name            =    str(info.get("name", ""))
                region_info.env_type        =    str(info.get("env", ""))
                region_info.title           =    str(info.get("title", ""))
                region_info.display_name    =    str(info.get("title", ""))
                region_info.dispatch_url    =    str(info.get("dispatchUrl", ""))

            updateRegionList.region_list.extend(response.region_list)
            
            serialized_data = updateRegionList.SerializeToString()
            base64_str = b64encode(serialized_data).decode()

            return base64_str
        else:
            code = 3
            content = "retcode"
            return returnJsonMsg_short(content, code)
    except Exception as err:
        code = 404
        msg = "not found"
        logger.error(err)
        return returnJsonMsg(code, msg, "")
