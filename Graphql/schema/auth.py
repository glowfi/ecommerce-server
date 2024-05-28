import strawberry


@strawberry.input
class InputLogin:
    email: str
    password: str
    userType: str


@strawberry.type
class Login:
    id: str
    accToken: str
    email: str
    userType: str


@strawberry.type
class LoginResponse:
    data: Login | None
    err: str | None


@strawberry.type
class RegisterResponse(LoginResponse):
    pass
