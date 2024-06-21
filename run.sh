#!/usr/bin/env bash

WORKERS=8
PORT=5000

echo "Production build!"

# Clean pycache
find . | grep *__pycache__/ | xargs -I "{}" rm -rf "{}"

# Remove print statements
remove-print-statements ./**/*.py

# Start Web app
gunicorn main:app -w "${WORKERS}" -k uvicorn.workers.UvicornWorker
