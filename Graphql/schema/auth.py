import strawberry

from Graphql.schema.user import Address


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
    address: Address
    userType: str
    phone_number: str


@strawberry.type
class LoginResponse:
    data: Login | None
    err: str | None


@strawberry.type
class LogoutResponse:
    data: str | None
    err: str | None


@strawberry.type
class RegisterResponse(LoginResponse):
    pass
