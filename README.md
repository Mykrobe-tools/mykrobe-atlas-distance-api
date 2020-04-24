[![Build Status](https://travis-ci.com/iqbal-lab-org/dist-api-prototype.svg?branch=master)](https://travis-ci.com/iqbal-lab-org/dist-api-prototype)

# Usage

## Start the development server
```shell script
docker build -t dist .
mkdir data
chown 101:101 data
./scripts/run.sh
```

## Load toy db
```shell script
cp backups/init.db.bak data/
docker exec -ti dist neo4j-admin load --from=/data/init.db.bak
```

## Or init a toy graph (20 minutes on 8 CPUs)
```shell script
docker exec -ti dist python3 -m swagger_server.initdb
```

## View the toy graph
* Visit http://localhost:7474
* Set `Connect URL` to `bolt://localhost:7687`
* Set `Authentication type` to `No authentication`
* Click the top left icon (Databases), it should show the currently existing node and relationship types. Click on one of them to view the graph.
* Drag the nodes far away from each other for clarity. You can also set colors for them.

## Make a test request

* Nearest neighbors
```shell script
curl --request GET 'localhost:8080/api/v1/samples/s1/nearest-neighbours'
# The result should be a JSON array of {experiement_id: str, distance: int}
```

* Nearest leaf in the phylogenetic tree
```shell script
curl --request GET 'localhost:8080/api/v1/samples/s1/nearest-leaf-node'
# The result should look like
# {
#   "distance": 7,
#   "leaf_id": "l857"
# }
```

## Stop (& destroy) the development server
```shell script
docker stop dist
```

# Development

## Run tests
```shell script
pip3 install tox
tox
```

## Run individual tests
```shell script
nosetests --nologcapture swagger_server/test/<test_file>:<TestClass>.<test_method>
```
https://nose.readthedocs.io/en/latest/usage.html#extended-usage
