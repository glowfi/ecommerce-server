from helper.krypt import _decrypt


class ModifyRequestBodyMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def modify_body():
            message = await receive()
            assert message["type"] == "http.request"

            body: bytes = message.get("body", b"")
            body: str = body.decode()

            # print(body, "BODY")
            decrypted = _decrypt(body)
            message["body"] = decrypted.encode()
            return message

        await self.app(scope, modify_body, send)
