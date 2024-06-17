#!/usr/bin/env bash

WORKERS=8
PORT=5000

# Source .env file
export $(grep -v '^#' .env | xargs)

if [[ "$STAGE" == "local" ]]; then
	echo "$STAGE"
	source ./env/bin/activate
	fd . | grep *__pycache__/ | xargs -I "{}" rm -rf "{}"
	uvicorn main:app --host "localhost" --port "${PORT}" --log-level "info" --reload
else
	gunicorn main:app -w "${WORKERS}" -k uvicorn.workers.UvicornWorker
fi
