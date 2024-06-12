from typing import Union
import strawberry


@strawberry.input
class InputresetPassword:
    password: str
    token: str
    userid: Union[str, None]


@strawberry.type
class resetPassword:
    userid: str
    token: str


@strawberry.type
class resetPasswordResponse:
    data: resetPassword | None
    err: str | None
