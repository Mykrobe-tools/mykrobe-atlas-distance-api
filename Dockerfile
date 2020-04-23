FROM neo4j:3.5

RUN apt update
RUN apt install -y --no-install-recommends python3-pip python3-setuptools curl unzip sed

RUN pip3 install wheel supervisor

WORKDIR /usr/src/app
RUN chown neo4j .
USER neo4j

COPY scripts/docker/install_graph_ds_lib.sh .
RUN bash install_graph_ds_lib.sh

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["supervisord", "-n"]
