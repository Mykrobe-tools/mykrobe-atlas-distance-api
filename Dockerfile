FROM python:3.8-slim-buster

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
COPY swagger_server /usr/src/app/swagger_server
WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "-m", "swagger_server"]
