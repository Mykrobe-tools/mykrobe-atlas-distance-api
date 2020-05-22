#!/usr/bin/env bash

mypy --follow-imports=skip --ignore-missing-imports swagger_server/drivers swagger_server/ogm swagger_server/repositories