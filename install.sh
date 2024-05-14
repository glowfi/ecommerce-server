#!/usr/bin/env fish

python -m venv env
source ./env/bin/activate.fish
pip install fastapi 'strawberry-graphql[fastapi]' uvicorn gunicorn motor beanie python-dotenv
