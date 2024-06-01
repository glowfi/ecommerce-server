import strawberry


@strawberry.input
class InputresetPassword:
    password: str
    token: str


@strawberry.type
class resetPassword:
    userid: str
    token: str


@strawberry.type
class resetPasswordResponse:
    data: resetPassword | None
    err: str | None
