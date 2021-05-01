# Dockerfile

FROM python:3.8-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD uwsgi uwsgi.ini
