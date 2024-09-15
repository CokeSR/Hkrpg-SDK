# 纯SDK环境
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /opt/hkrpg/sdkserver/
RUN pip install --no-cache-dir -r /opt/hkrpg/sdkserver/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /opt/hkrpg/sdkserver
EXPOSE 21000

CMD [ "python", "./main.py"]
