import yaml
import src.system.response.retcode as rep

from src.system.logging.systemctl   import logger as syslog

def configRebuild() -> str:
    try:
        config = {
            "App": {
                # Default settings
                "ssl": False,
                "host": "0.0.0.0",
                "port": 1234,
                "reload": False,
                "debug": False,
                "threaded": False,
            },
            "Database": {
                "mysql": {
                    "host": "",
                    "user": "",
                    "port": "",
                    "auto_rebuild": True,
                    "db_name": "",
                    "password": "",
                },
            },
            "Api": {
                "modified": False,
                "protocol": False,
                "qr_enabled": False,
                "enable_user_center": False,
                "disable_ysdk_guard": False,
                "enable_announce_pic_popup": False,
                "enable_web_dpi": False,
                "list_price_tierv2_enable": False,
                "modify_real_name_other_verify": False,
                "sceneWhiteList": False,
                "experimentWhiteList": False,
                "device_grant_required": False,
                "safe_moblie_required": False,
                "realperson_required": False,
                "reactivate_required": False,
            },
            "Client": {
                "guest": False,
                "heartbeat": False,
                "disable_regist": False,
                "enable_email_captcha": False,
                "disable_mmt": False,
                "server_guest": False,
                "enable_ps_bind_account": False,
                "initialize_firebase": False,
                "bbs_auth_login": False,
                "fetch_instance_id": False,
                "enable_flash_login": False,
                "enable_logo_18": False,
                "enable_cx_bind_account": False,
                "firebase_blacklist_devices_switch": False,
                "hoyolab_auth_login": False,
                "hoyoplay_auth_login": False,
            },
            "Security": {
                "is_sign": False,
                "sign_key": "",
                "verify_code_length": 4,
                "min_password_len": 8,
            },
            "Region": [
                {
                    "env": "",
                    "title": "",
                    "name": "",
                    "dispatchUrl": "",
                }
            ],
            "Mail": {
                "enable": False,
                "mail_server": "",
                "mail_port": "",
                "mail_username": "",
                "mail_pasword": "",
                "mail_sender": "",
            },
        }
        with open(rep.CONFIG_PATH, "wb") as f:
            yaml.dump(config, f, encoding="utf-8", sort_keys=False)
        syslog.info(f"{'=' * 15} AUTO REBUILD CONFIG SUCC {'=' * 15}")
        return "Done."

    except Exception as err:
        syslog.error(f"Can't rebuild config: {err}")
        syslog.error(f"{'=' * 15} AUTO REBUILD CONFIG FAILED {'=' * 15}")
