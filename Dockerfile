FROM neo4j:3.5

RUN apt update
RUN apt install -y --no-install-recommends python3-pip python3-setuptools curl unzip

RUN pip3 install wheel supervisor

WORKDIR /usr/src/app
RUN chown neo4j .
USER neo4j

RUN curl -k -LO https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/graph-data-science/neo4j-graph-data-science-1.1.0-standalone.zip
RUN unzip -d $NEO4J_HOME/plugins neo4j-graph-data-science-1.1.0-standalone.zip
COPY conf/neo4j.conf $NEO4J_HOME/conf/

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["supervisord", "-n"]
