import os
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from dotenv import find_dotenv, load_dotenv

# Load dotenv
load_dotenv(find_dotenv(".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


class JWTManager:

    @staticmethod
    async def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=float(expires_delta))

        else:
            expire = datetime.utcnow() + timedelta(
                minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    @staticmethod
    async def verify_jwt(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_timestamp = datetime.utcnow().timestamp()
            if not decode_token:
                raise ValueError("Invalid token!")
            elif decode_token["exp"] <= current_timestamp:
                raise ValueError("Token expired!")
            return True
        except ValueError as error:
            print(error)
            return False

    @staticmethod
    async def get_token_data(token: str) -> dict | None:
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_timestamp = datetime.utcnow().timestamp()
            if decode_token["exp"] <= current_timestamp:
                raise ValueError("Token expired!")
            return decode_token
        except ValueError as error:
            print(error)
            return None
