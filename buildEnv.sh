#!/bin/sh

envPatch="/opt/sdk"

sudo apt update && sudo apt apt upgrade -y
sudo apt install python-is-python3 -y
sudo pip install python3-pip -y 

cd $envPatch
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
