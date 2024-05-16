import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Reviews:
    id: str
    comment: str
    user_reviewed: Annotated["User", strawberry.lazy(".user")]
    product_reviewed: Annotated["Product", strawberry.lazy(".product")]
    reviewedAt: datetime


@strawberry.input
class InputReviews:
    userID: str
    productID: str
    comment: str


@strawberry.input
class InputUpdateReviews:
    reviewID: str
    comment: str


@strawberry.type
class ResponseReviews:
    data: Reviews | None
    err: str | None


@strawberry.type
class ResponseGetallReviews:
    data: list[Reviews] | None
    err: str | None
