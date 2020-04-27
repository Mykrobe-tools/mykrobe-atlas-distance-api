#!/usr/bin/env bash

docker exec -ti dist tail -f app_stdout.log app_stderr.log
