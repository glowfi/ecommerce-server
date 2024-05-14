#!/usr/bin/env bash

WORKERS=8
PORT=5000

gunicorn main:app -w "${WORKERS}" -b 0.0.0.0:"${PORT}" -k uvicorn.workers.UvicornWorker --log-file=- --log-level DEBUG --reload
