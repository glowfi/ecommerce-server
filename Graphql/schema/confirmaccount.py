import strawberry


@strawberry.type
class ConfirmAccount:
    data: str | None
    err: str | None
