import strawberry

from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .orders import Orders
    from .wishlist import Wishlist
    from .reviews import Reviews


@strawberry.type
class User:
    email: str
    name: str
    password: str
    dob: str
    phone_number: str
    address: str
    wishlist: list[Annotated["Wishlist", strawberry.lazy(".wishlist")]]
    orders: list[Annotated["Orders", strawberry.lazy(".orders")]]
    reviews: list[Annotated["Reviews", strawberry.lazy(".reviews")]]
