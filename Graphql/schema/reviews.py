from pydantic import BaseModel, ConfigDict
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
    productId: str
    userId: str
    reviewedAt: datetime


@strawberry.input
class InputReviews:
    userID: str
    productID: str
    comment: str


@strawberry.input
class InputUpdateReviews:
    comment: str


@strawberry.type
class ResponseReviews:
    data: Reviews | None
    err: str | None


@strawberry.type
class ResponseGetallReviews:
    data: list[Reviews] | None
    err: str | None
