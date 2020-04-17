FROM neo4j:3.5

RUN apt update
RUN apt install -y --no-install-recommends python3-pip python3-setuptools

RUN pip3 install wheel supervisor

WORKDIR /usr/src/app
RUN chown neo4j .

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["supervisord", "-n"]
