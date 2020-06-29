[![Build Status](https://travis-ci.com/iqbal-lab-org/dist-api-prototype.svg?branch=master)](https://travis-ci.com/iqbal-lab-org/dist-api-prototype)

# Usage

## Start the development server
```shell script
docker build -t dist .
./scripts/run.sh
```
The script create a `./data` directory to persist Neo4j's data to the host machine. The Docker image will load a sample database if the directory `./data/databases/graph.db` does not exist (for example, at first run).

If you want to restore the sample data, simply delete `./data` and run `./scripts/run.sh` again.

## Init a new sample database (20 seconds on 8 CPUs)
```shell script
./scripts/regenerate_db.sh
```

## Backup the current db
```shell script
./scripts/backup_db.sh # will dump to ./data/init.db.bak on host machine
```

## Tail application's logs
```shell script
make logs
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
make test_db
make test
```
