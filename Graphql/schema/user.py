import strawberry

from typing import TYPE_CHECKING, Annotated, Optional

if TYPE_CHECKING:
    from .orders import Orders
    from .wishlist import Wishlist
    from .reviews import Reviews


@strawberry.type
class User:
    id: str
    email: str
    name: str
    password: str
    dob: str
    phone_number: str
    address: str
    wishlist: list[Annotated["Wishlist", strawberry.lazy(".wishlist")]]
    orders: list[Annotated["Orders", strawberry.lazy(".orders")]]
    reviews: list[Annotated["Reviews", strawberry.lazy(".reviews")]]


@strawberry.input
class InputUser:
    email: str
    name: str
    password: str
    dob: str
    phone_number: str
    address: str


@strawberry.input
class InputUpdateUser:
    userID: str
    email: Optional[str]
    name: Optional[str]
    password: Optional[str]
    dob: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]


@strawberry.type
class ResponseUser:
    data: User | None
    err: str | None


@strawberry.type
class ResponseGetallUser:
    data: list[User] | None
    err: str | None
