#!/usr/bin/env bash

WORKERS=8
PORT=5000

if [[ "$STAGE" != "production" ]]; then
	echo "Local build!"
	source ./env/bin/activate
	fd . | grep *__pycache__/ | xargs -I "{}" rm -rf "{}"
	uvicorn main:app --host "localhost" --port "${PORT}" --log-level "info" --reload
else
	echo "Production build!"
	fd . | grep *__pycache__/ | xargs -I "{}" rm -rf "{}"
	gunicorn main:app -w "${WORKERS}" -b 0.0.0.0:"${PORT}" -k uvicorn.workers.UvicornWorker
fi
