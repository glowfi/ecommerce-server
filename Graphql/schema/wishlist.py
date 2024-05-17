import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Wishlist:
    id: str
    user_wished: Annotated["User", strawberry.lazy(".user")]
    product_wished: Annotated["Product", strawberry.lazy(".product")]
    wishedAt: datetime


@strawberry.input
class InputWishlist:
    userID: str
    productID: str


# @strawberry.input
# class InputUpdateWishlist:
#     pass


@strawberry.type
class ResponseWishlist:
    data: Wishlist | None
    err: str | None


@strawberry.type
class ResponseGetallWishlist:
    data: list[Wishlist] | None
    err: str | None
