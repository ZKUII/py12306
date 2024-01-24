FROM python:3.8.10-slim

ENV TZ Asia/Shanghai

WORKDIR /code

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir -p /data/query /data/user
VOLUME /data

COPY . .

COPY env.py /config/env.py

CMD [ "python", "main.py" , "-c", "/config/env.py"]
