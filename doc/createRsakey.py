import os
from Crypto.PublicKey import RSA

key = RSA.generate(2048)

private_key = key.export_key()
public_key = key.publickey().export_key()

main_path            = os.getcwd()
rsa_public_key_path  = f"{main_path}/data/api/public.key"
rsa_private_key_path = f"{main_path}/data/api/private.key"

try:
    with open(rsa_private_key_path, 'w', encoding="utf-8") as file:
        data = private_key.decode()
        file.write(data)
        file.close()

    with open(rsa_public_key_path, 'w', encoding="utf-8") as file:
        data = public_key.decode()
        file.write(data)
        file.close()
    
    print(f"Create rsa keys succ")
except Exception as err:
    print(f"Create rsa keys fail: {err}")
