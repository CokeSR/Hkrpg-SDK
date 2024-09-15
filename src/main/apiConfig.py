from __main__                       import app
from flask                          import abort, request
from urllib.parse                   import urlencode
from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig
from src.system.response.jsonMsg    import (
    returnJsonMsg,
    returnJsonMsg_create, 
    returnJsonMsg_short,
)

import src.system.response.retcode as retcode

@app.route('/admin/mi18n/plat_oversea/m202003049/<version>-version.json', methods = ['GET'])
@app.route('/admin/mi18n/plat_oversea/m202003049/<version>-zh-cn.json', methods = ['GET'])
@app.route('/admin/mi18n/plat_oversea/m2020030410/<version>-version.json', methods = ['GET'])
@app.route('/admin/mi18n/plat_oversea/m2020030410/<version>-zh-cn.json', methods = ['GET'])
def adminMi18n_plat_oversea(version):
    logger.info(f"Request:{request.url_rule} , mi18n version: {version}")
    if version == "m2020030410" or "m202003049":
        msg = returnJsonMsg_short("version", 96)
        return msg
    else:
        logger.error(f"Request mi18n version fail: {version}")
        return abort(404)


@app.route('/admin/mi18n/plat_os/m09291531181441/<version>-version.json', methods = ['GET'])
@app.route('/admin/mi18n/plat_os/m09291531181441/<version>-zh-cn.json', methods = ['GET'])
def adminMi18n_plat_os(version):
    logger.info(f"Request:{request.url_rule} , mi18n version: {version}")
    if version == "m09291531181441":
        msg = returnJsonMsg_short("version", 16)
        return msg
    else:
        logger.error(f"Request mi18n version fail: {version}")
        return abort(404)


# app_id=8 channel_id=1 client_type=3
@app.route('/hkrpg_cn/combo/granter/api/getConfig', methods = ['GET'])
@app.route('/hkrpg_global/combo/granter/api/getConfig', methods = ['GET'])
def getApiConfig():
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        app_id = request.args.get('app_id')
        channel_id = request.args.get('channel_id')
        client_type = request.args.get('client_type')
        if (app_id  and channel_id  and client_type):
            config = getConfig()['Api']
            content = {
                    "protocol": config['protocol'],
                    "qr_enabled": config['qr_enabled'],
                    "log_level": "INFO",
                    "announce_url": "https://sdk.mihoyo.com/hkrpg/announcement/index.html?sdk_presentation_style=fullscreen&game=hkrpg&game_biz=hkrpg_cn&sdk_screen_transparent=True&auth_appid=announcement&authkey_ver=1&version=2.28&sign_type=2#/",
                    "push_alias_type": 1,
                    "disable_ysdk_guard": config['disable_ysdk_guard'],
                    "enable_announce_pic_popup": config['enable_announce_pic_popup'],
                    "app_name": "崩坏:星穹铁道",
                    "qr_enabled_apps": {
                    "bbs": True,
                    "cloud": True
                },
                "qr_app_icons": {
                    "app": "https://sdk-webstatic.mihoyo.com/sdk-public/2023/10/11/63b6857bddb8be0887185890596b983f_4890465413038841959.png",
                    "bbs": "https://sdk-webstatic.mihoyo.com/sdk-public/2023/10/11/69172b1a1fd17290b3e0649632216372_106775796556262449.png",
                    "cloud": "https://sdk-webstatic.mihoyo.com/sdk-public/2024/01/10/7ba59a037e1052383005401a107ac6e2_5105971712612688683.png"
                },
                "qr_cloud_display_name": "云•星穹铁道",
                "enable_user_center": config['enable_user_center'],
                "functional_switch_configs": {}
            }
            return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
        else:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "参数错误")
    except Exception:
        return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "未知参数")


# biz_key=hkrpg_cn client_type=3
@app.route('/combo/box/api/config/sdk/combo', methods = ['GET'])
def comboBox():
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        biz = request.args.get('biz_key')
        client_type = request.args.get('client_type')
        if (biz  and client_type):
            config = getConfig()['Api']
            content = {
                    "vals": {
                        "telemetry_config": {
                            'dataupload_enable': 1
                        },
                        "enable_web_dpi": config['enable_web_dpi'],
                        "h5log_filter_config": {
                            "function": {
                                "event_name": [
                                    "info_get_cps", 
                                    "notice_close_notice", 
                                    "info_get_uapc", 
                                    "report_set_info", 
                                    "info_get_channel_id", 
                                    "info_get_sub_channel_id"
                                ]
                            }
                        },
                        "webview_rendermethod_config": {
                            "useLegacy":True
                        },
                        "list_price_tierv2_enable": config['list_price_tierv2_enable'],
                        "kibana_pc_config": { "enable": 1, "level": "Info","modules": ["download"]},
                        "network_report_config": {"enable": 1, "status_codes": [206], "url_paths": ["dataUpload", "red_dot"] },
                        "modify_real_name_other_verify": config['modify_real_name_other_verify']
                }
            }
            return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
        else:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "参数错误")
    except Exception:
        return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "未知参数")


# platform=3
@app.route('/device-fp/api/getExtList', methods = ['GET'])
def getExtlist():
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        platfrom = request.args.get('platfrom')
        if (platfrom):
            content = {
                "code": retcode.SETTINGS_SUCC,
                "msg": "ok",
                "ext_list": [
                    "cpuName",
                    "deviceModel",
                    "deviceName",
                    "deviceType",
                    "deviceUID",
                    "gpuID",
                    "gpuName",
                    "gpuAPI",
                    "gpuVendor",
                    "gpuVersion",
                    "gpuMemory",
                    "osVersion",
                    "cpuCores",
                    "cpuFrequency",
                    "gpuVendorID",
                    "isGpuMultiTread",
                    "memorySize",
                    "screenSize",
                    "engineName",
                    "addressMAC",
                    "packageVersion",
                ],
                "pkg_list": [],
                "pkg_str": "",
            }
            return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
        else:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "参数错误")
    except Exception:
        return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "未知参数")


# client=3 game_key=hkrpg_cn
@app.route('/hkrpg_cn/mdk/shield/api/loadConfig', methods = ['GET'])
@app.route('/hkrpg_global/mdk/shield/api/loadConfig', methods = ['GET'])
def clientConfig():
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        client = request.args.get("client")
        game_key = request.args.get("game_key")
        if (client  and game_key):
            config = getConfig()['Client']
            content = {
                "id": 21,
                "game_key": "hkrpg_cn",
                "client": retcode.PLATFORM_TYPE[int(client)],     # client = 3
                "identity": "I_IDENTITY",
                "guest": config['guest'],
                "ignore_versions": "",
                "scene": "S_NORMAL",
                "name": "崩坏RPG",
                "disable_regist": config['disable_regist'],
                "enable_email_captcha": config['enable_email_captcha'],
                "thirdparty": ["tp"],
                "disable_mmt": config['disable_mmt'],
                "server_guest": config['server_guest'],
                "thirdparty_ignore": {},
                "enable_ps_bind_account": config['enable_ps_bind_account'],
                "thirdparty_login_configs": {},
                "initialize_firebase": config['initialize_firebase'],
                "bbs_auth_login": config['bbs_auth_login'],
                "bbs_auth_login_ignore": [],
                "fetch_instance_id": config['fetch_instance_id'],
                "enable_flash_login": config['enable_flash_login'],
                "enable_logo_18": config['enable_logo_18'],
                "logo_height": "0",
                "logo_width": "0",
                "enable_cx_bind_account": config['enable_cx_bind_account'],
                "firebase_blacklist_devices_switch": config['firebase_blacklist_devices_switch'],
                "firebase_blacklist_devices_version": 0,
                "hoyolab_auth_login": config['hoyolab_auth_login'],
                "hoyolab_auth_login_ignore": [],
                "hoyoplay_auth_login": config['hoyoplay_auth_login'],
            }
            return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
        else:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "参数错误")
    except Exception:
        return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "未知参数")


# biz=hkrpg_cn client=3
@app.route('/combo/box/api/config/sw/precache', methods = ['GET'])
def precache():
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    try:
        biz = request.args.get('biz')
        client = request.args.get('client')
        if (biz  and client):
            return returnJsonMsg(retcode.SETTINGS_NO_CONFIG, "RetCode_NoConfig", "")
        else:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "参数错误")
    except Exception:
        return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "未知参数")


@app.route("/data_abtest_api/config/experiment/list", methods=['POST'])
def experimentList():
    logger.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    config = getConfig()['Api']
    content = [
        {
            "code": 1000,
            "type": 2,
            "config_id": "284",
            "period_id": "5277_581",
            "version": "2",
            "configs": {
                "cardType": "native",
                "cashierId": "4b1ca92d-acc0-4a93-afb2-b3e3b5c0ac65",
            },
            "sceneWhiteList": config['sceneWhiteList'],
            "experimentWhiteList": config['experimentWhiteList'],
        },
        {
            "code": 1000,
            "type": 2,
            "config_id": "245",
            "period_id": "5145_536",
            "version": "2",
            "configs": {"foldOther": "False"},
            "sceneWhiteList": config['sceneWhiteList'],
            "experimentWhiteList": config['experimentWhiteList'],
        },
        {
            "code": 1000,
            "type": 2,
            "config_id": "244",
            "period_id": "5144_535",
            "version": "1",
            "configs": {"expandMixedQRcode": "true"},
            "sceneWhiteList": config['sceneWhiteList'],
            "experimentWhiteList": config['experimentWhiteList'],
        },
        {
            "code": 1010,
            "type": 2,
            "config_id": "243",
            "period_id": "",
            "version": "",
            "configs": {"disableMarket": "False"},
            "sceneWhiteList": config['sceneWhiteList'],
            "experimentWhiteList": config['experimentWhiteList'],
        },
        {
            "code": 1000,
            "type": 2,
            "config_id": "288",
            "period_id": "5281_629",
            "version": "2",
            "configs": {"cashierPreload": "true"},
            "sceneWhiteList": config['sceneWhiteList'],
            "experimentWhiteList": config['experimentWhiteList'],
        },
        {
            "code": 1000,
            "type": 2,
            "config_id": "287",
            "period_id": "5280_628",
            "version": "1",
            "configs": {"levelQRCode": "L"},
            "sceneWhiteList": config['sceneWhiteList'],
            "experimentWhiteList": config['experimentWhiteList'],
        },
    ]
    return returnJsonMsg(retcode.RESPONSE_SUCC, "true", content)


# {"device_id":"21a999314330ae5414dd63b17f3429525990d3e91711718364684","seed_id":"4609938928515028","seed_time":"1711718377857","platform":"3","device_fp":"38d7f8602cc57","app_name":"hkrpg_cn","ext_fields":"{\"osVersion\":\"Windows 10  (10.0.19045) 64bit\",\"deviceModel\":\"Vivobook_ASUSLaptop K6500ZC_K6500ZC (ASUSTeK COMPUTER INC.)\",\"deviceName\":\"DESKTOP-AU41B5O\",\"deviceType\":\"Desktop\",\"deviceUID\":\"21a999314330ae5414dd63b17f3429525990d3e9\",\"cpuName\":\"12th Gen Intel(R) Core(TM) i5-12500H\",\"cpuCores\":16,\"cpuFrequency\":\"3110\",\"gpuID\":\"9634\",\"gpuName\":\"NVIDIA GeForce RTX 3050 Laptop GPU\",\"gpuAPI\":\"Direct3D11\",\"gpuVendor\":\"NVIDIA\",\"gpuVersion\":\"Direct3D 11.0 [level 11.1]\",\"gpuMemory\":\"3964\",\"gpuVendorID\":4318,\"isGpuMultiTread\":false,\"memorySize\":16074,\"screenSize\":\"1920*1080\",\"engineName\":\"Unity\",\"addressMAC\":\"EAFB1C7E6C4F\",\"packageVersion\":\"2.27.0.0\"}"}
@app.route('/device-fp/api/getFp', methods = ['POST'])
def getFP():
    logger.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    try:
        device_fp = request.json['device_fp']
        if device_fp :
            content = {
                "device_fp": device_fp,
                "code": retcode.SETTINGS_SUCC,
                "msg": "ok"
            }
            return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
        else:
            return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "参数错误")
    except Exception:
        return returnJsonMsg(retcode.RESPONSE_FAIL, "error", "未知参数")
    

@app.route('/hkrpg_cn/combo/granter/api/compareProtocolVersion', methods = ['POST'])
@app.route('/hkrpg_global/combo/granter/api/compareProtocolVersion', methods = ['POST'])
def compareProtocolVersion():
    logger.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    config = getConfig()['Api']
    content = {
        "modified": config['modified'],
        "protocol": None
    }
    return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)


@app.route("/_ts", methods = ['GET'])
def TS():
    logger.info(f"Request:{request.url_rule} , MSG:?{urlencode(request.values.to_dict())}")
    return returnJsonMsg_create(retcode.RESPONSE_SUCC, "app running")


@app.route("/account/risky/api/check", methods=["POST"])
def account_risky_api_check():
    logger.info(f"Request:{request.url_rule} , MSG:{request.data.decode()}")
    content = {
            "id": "none",
            "action": retcode.RISKY_ACTION_NONE,
            "geetest": None,
    }
    return returnJsonMsg(retcode.RESPONSE_SUCC, "OK", content)
