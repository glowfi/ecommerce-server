import strawberry


@strawberry.type
class Admin:
    id: str
    email: str
    password: str


@strawberry.input
class InputAdmin:
    email: str
    password: str


@strawberry.type
class ResponseAdmin:
    data: Admin | None
    err: str | None
