from typing import Optional
import strawberry


@strawberry.input
class InputresetPassword:
    password: str
    token: str
    userid: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class resetPassword:
    userid: str
    token: str


@strawberry.type
class resetPasswordResponse:
    data: resetPassword | None
    err: str | None
