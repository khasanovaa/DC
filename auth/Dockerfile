FROM python:latest

ADD requirements.txt /app/
RUN apt-get update \
    && apt-get clean \
    && apt-get update -qqq \
    && pip install --upgrade pip \ 
    && pip install -r /app/requirements.txt

ADD *.py /server/

WORKDIR /server/
