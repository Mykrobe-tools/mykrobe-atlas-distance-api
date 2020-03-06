```shell script
docker build -t dist .
docker run --rm -it -p 8080:8080 --name dist dist
# wait until seeing sth like this: INFO success: app entered RUNNING state

# in another shell
curl --request POST \
  --url http://localhost:8080/distance \
  --header 'content-type: application/json' \
  --data '{
	"experiment_id": "SAMEA3281408"
}'
```
