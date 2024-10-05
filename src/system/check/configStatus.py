from src.system.logging.systemctl   import logger
from src.system.loading.config      import getConfig

def checkConfig() -> bool:
    config = getConfig()
    required_settings = {
        "App": {
            "ssl": bool,
            "host": str,
            "port": int,
            "reload": bool,
            "debug": bool,
            "threaded": bool,
        },
        "Database": {
            "mysql": {
                "host": str,
                "user": str,
                "port": int,
                "auto_rebuild": bool,
                "db_name": str,
                "password": str,
            },
        },
        "Api": {
            "modified": bool,
            "protocol": bool,
            "qr_enabled": bool,
            "enable_user_center": bool,
            "disable_ysdk_guard": bool,
            "enable_announce_pic_popup": bool,
            "enable_web_dpi": bool,
            "list_price_tierv2_enable": bool,
            "modify_real_name_other_verify": bool,
            "sceneWhiteList": bool,
            "experimentWhiteList": bool,
            "device_grant_required": bool,
            "safe_moblie_required": bool,
            "realperson_required": bool,
            "reactivate_required": bool,
        },
        "Client": {
            "guest": bool,
            "heartbeat": bool,
            "disable_regist": bool,
            "enable_email_captcha": bool,
            "disable_mmt": bool,
            "server_guest": bool,
            "enable_ps_bind_account": bool,
            "initialize_firebase": bool,
            "bbs_auth_login": bool,
            "fetch_instance_id": bool,
            "enable_flash_login": bool,
            "enable_logo_18": bool,
            "enable_cx_bind_account": bool,
            "firebase_blacklist_devices_switch": bool,
            "hoyolab_auth_login": bool,
            "hoyoplay_auth_login": bool,
        },
        "Security": {
            "is_sign": bool,
            "sign_key": str,
            "verify_code_length": int,
            "min_password_len": int,
        },
        "Region": { },
        "Mail": {
            "enable": bool,
            "mail_server": str,
            "mail_port": int,
            "mail_username": str,
            "mail_pasword": str,
            "mail_sender": str,
        },
    }

    missing_keys = []
    invalid_type_keys = []

    # 递归检查
    def check_settings(config_section, required_settings_section, path):
        
        if isinstance(required_settings_section, dict):
            for key, expected_type in required_settings_section.items():
                if key not in config_section:
                    missing_keys.append(f"Config item is missing: {path}.{key}")
                else:
                    logger.info(f"Loading config item: '{path}.{key}': '{config_section[key]}'")
                    if isinstance(expected_type, dict):
                        check_settings(config_section[key], expected_type, f"{path}.{key}")
                    else:
                        if not isinstance(config_section[key], expected_type):
                            invalid_type_keys.append(f"Unknown configuration: {path}.{key}, The vaule: {config_section[key]} (Must be {expected_type.__name__})")

        elif isinstance(required_settings_section, list):
            for setting in required_settings_section:
                if setting not in config_section:
                    missing_keys.append(f"{path}.{setting}")

    # 细节
    for section, settings in required_settings.items():
        if section not in config:
            missing_keys.append(section)
        else:
            check_settings(config[section], settings, section)

    if missing_keys or invalid_type_keys:
        if missing_keys:
            logger.error(f"".join(missing_keys))
        if invalid_type_keys:
            logger.error(f"".join(invalid_type_keys))
        return False

    logger.info(f"{'=' * 15} LOADING CONFIG SUCC {'=' * 15}")
    return True


def checkRegion() -> bool:
    try:
        for entry in getConfig()["Region"]:
            logger.info(f"Load dispatch region: {entry}")
            if (
                "env" not in entry
                or "title" not in entry
                or "name" not in entry
                or "dispatchUrl" not in entry
            ):
                logger.error(f"There are items in the configuration table that are empty or incomplete")
                return False
    except:
        logger.error(f"The configuration item is corrupted or missing")
        return False
    logger.info(f"{'=' * 15} LOADING DISPATCH REGION SUCC {'=' * 15}")
    return True
