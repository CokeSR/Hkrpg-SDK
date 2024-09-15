import yaml
import src.system.response.retcode as code


def getConfig() -> str:
    with open(code.CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
