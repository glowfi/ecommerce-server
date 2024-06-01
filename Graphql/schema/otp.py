from datetime import datetime
import strawberry


@strawberry.input
class OTPInput:
    token: str


@strawberry.type
class OTP:
    userID: str
    token: str
    lastUsed: datetime
    hasExpired: bool


@strawberry.type
class OTPResponse:
    data: OTP | None
    err: str | None
