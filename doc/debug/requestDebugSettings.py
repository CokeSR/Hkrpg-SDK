import os
import time
import base64

from Crypto.Cipher      import PKCS1_OAEP
from Crypto.PublicKey   import RSA
import requests

proto     = "http"
address   = "127.0.0.1"
port      = 1234
route     = "develop/showUsers"
path      = f"{os.getcwd()}/data/api/public.key"
timestamp = int(time.time())

def createSignKey(sign, timestamp, cmd, ticket="cokeserver") -> str:
    url = [f"sign={sign}", f"time={timestamp}", f"cmd={cmd}", f"ticket@{ticket}"]
    request_url = "&".join(url)
    # base64 / python3
    # base64_encode = base64.b64encode(request_url.encode('utf-8')).decode()

    with open(path, 'r', encoding="UTF-8") as file:
        public_key = file.read()

    # 加密对象
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_msg = cipher.encrypt(request_url.encode())

    # base64 / python3
    encrypted_msg_b64 = base64.b64encode(encrypted_msg).decode('utf-8')

    url = f"{proto}://{address}:{port}/{route}?cmd={cmd}&sign={encrypted_msg_b64}"
    return url


def requestDebugSettings(url) -> str:
    request = requests.get(url)
    return request.text


if __name__ == "__main__":
    cmd       = "showUsers"
    sign      = "cDyN1GXyw1LRx8R66Tl0tBSjysIXMxnvfkXFqO9DMT3eT0EYjM3dHqEaqmzLEwCj"
    url       =  createSignKey(sign, timestamp, cmd)
    print(f"请求: {url}") 
    print(f"回显: {requestDebugSettings(url)}")
