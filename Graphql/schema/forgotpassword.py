import strawberry


@strawberry.input
class InputForgotPassword:
    email: str
    userType: str
    browser: str
    os: str


@strawberry.type
class ForgotPassword:
    email: str
    userType: str
    browser: str
    os: str
    token: str


@strawberry.type
class ForgotPasswordResponse:
    data: ForgotPassword | None
    err: str | None
