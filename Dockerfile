FROM neo4j

RUN apt update
RUN apt install -y --no-install-recommends build-essential zlib1g-dev libssl-dev libffi-dev curl

# Install Python 3.8
WORKDIR /tmp
RUN curl -O https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
RUN tar -xf Python-3.8.2.tar.xz
WORKDIR Python-3.8.2
RUN ./configure
RUN make
RUN make install
RUN rm -r /tmp/Python*

RUN pip3 install wheel supervisor

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

RUN chown neo4j .
USER neo4j

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["supervisord", "-n"]
