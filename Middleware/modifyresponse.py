import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message
import json
from helper.krypt import _encrypt
from dotenv import find_dotenv, load_dotenv

# Read dotenv
load_dotenv(find_dotenv(".env"))
secret = os.getenv("SECRET_REQ_RES")


class ModifyResponseBodyMiddleware(BaseHTTPMiddleware):
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        body = receive_.get("body")

        async def receive() -> Message:
            receive_["body"] = body
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):

        if request.method == "POST":
            await self.set_body(request)

        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        if response_body.decode().find("Strawberry GraphiQL"):
            try:
                data = json.loads(response_body.decode())
                res = data.get("data", {}).get("__schema", {}).get("queryType")
                if not res:
                    modified_response = _encrypt(secret, json.dumps(data))
                    return Response(
                        content=modified_response,
                        status_code=response.status_code,
                        media_type=response.media_type,
                    )
            except Exception as e:
                print(e)
            return Response(
                content=response_body,
                status_code=response.status_code,
                media_type=response.media_type,
            )
