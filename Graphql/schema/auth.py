import strawberry


@strawberry.input
class InputLogin:
    email: str
    password: str
    userType: str


@strawberry.type
class Login:
    userID: str
    accToken: str
    email: str
    profile_pic: str
    name: str
    userType: str


@strawberry.type
class LoginResponse:
    data: Login | None
    err: str | None


@strawberry.type
class RegisterResponse(LoginResponse):
    pass
