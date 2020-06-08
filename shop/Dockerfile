FROM python:latest

ADD shop/requirements.txt /app/
RUN apt-get update \
    && apt-get clean \
    && apt-get update -qqq \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt

ADD shop/*.py /shop/

ADD shop/idgen.txt /shop/