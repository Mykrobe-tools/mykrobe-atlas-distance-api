#!/usr/bin/env bash

java -jar scripts/swagger-codegen-cli.jar generate -o . -i swagger.yaml -l python-flask
