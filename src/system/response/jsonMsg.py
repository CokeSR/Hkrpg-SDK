import json

def returnJsonMsg(status_code, status, content) -> str:
    info = {
        "retcode": status_code,
        "message": status,
        "data": None if content == "" else content
    }
    message = json.loads(json.dumps(info))
    return message

def returnJsonMsg_short(index, key) -> str:
    info = {
        index: key
    }
    message = json.loads(json.dumps(info))
    return message

def returnJsonMsg_create(code, content) -> str:
    info = {
        "code": code,
        "message": content,
        "milliTs": "1725164968807"
    }
    message = json.loads(json.dumps(info))
    return message
