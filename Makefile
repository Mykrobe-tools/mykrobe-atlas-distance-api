generate:
	java -jar scripts/swagger-codegen-cli.jar generate -o . -i swagger.yaml -l python-flask

build:
	docker build -t dist .

type_check:
	mypy swagger_server

test_db:
	docker run --rm --name test_neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none neo4j

test:
	pytest

run:
	./scripts/run.sh

logs:
	docker exec -ti dist tail -f app_stdout.log app_stderr.log

clean:
	docker system prune -f && docker volume prune -f
