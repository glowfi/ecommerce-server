import strawberry


@strawberry.input
class InputForgotPassword:
    email: str
    userType: str


@strawberry.type
class ForgotPassword:
    email: str
    userType: str


@strawberry.type
class ForgotPasswordResponse:
    data: ForgotPassword | None
    err: str | None
