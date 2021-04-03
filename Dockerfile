# Dockerfile

FROM python:3.8-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN alembic upgrade head

ENTRYPOINT ["python"]
CMD ["app.py"]
