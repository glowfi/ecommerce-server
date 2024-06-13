from pydantic import BaseModel, ConfigDict
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional, Union

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Reviews:
    id: str
    comment: str
    rating: int
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
    rating: int


@strawberry.type
class ReviewsPercentage:
    totalReviews: Union[int, None]
    oneStars: Union[float, None]
    twoStars: Union[float, None]
    threeStars: Union[float, None]
    fourStars: Union[float, None]
    fiveStars: Union[float, None]


@strawberry.type
class ReviewsPercentageResponse:
    data: ReviewsPercentage | None
    err: str | None


@strawberry.input
class InputUpdateReviews:
    userID: Union[str, None]
    productID: Union[str, None]
    comment: Union[str, None]
    rating: Union[int, None]


@strawberry.type
class ResponseReviews:
    data: Reviews | None
    err: str | None


@strawberry.type
class ResponseGetallReviews:
    data: list[Reviews] | None
    err: str | None
