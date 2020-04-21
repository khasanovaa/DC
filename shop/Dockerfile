FROM python:latest

ADD shop/requirements.txt /app/
RUN apt-get update \
    && apt-get clean \
    && apt-get update -qqq \
    && pip install --upgrade pip \ 
    && pip install -r /app/requirements.txt

ADD shop/server.py /shop/

ADD shop/Database.py /shop/

ADD shop/config.py /shop/

ADD auth/authconfig.py /shop/


#WORKDIR /shop/


