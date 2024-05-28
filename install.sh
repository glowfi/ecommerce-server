#!/usr/bin/env fish

# Cleanup
rm -rf env
bash -c 'fd . | grep *__pycache__/ | xargs -I "{}" rm -rf "{}"'

# Install
python -m venv env
source ./env/bin/activate.fish
pip install fastapi 'strawberry-graphql[fastapi]' uvicorn gunicorn motor beanie python-dotenv python-jose[cryptography] faker redis resend
