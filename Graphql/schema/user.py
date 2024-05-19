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
    dob: Optional[str] = strawberry.field(default_factory=str)
    phone_number: Optional[str] = strawberry.field(default_factory=str)
    address: Optional[str] = strawberry.field(default_factory=str)


@strawberry.input
class InputUpdateUser:
    email: Optional[str] = strawberry.field(default_factory=str)
    name: Optional[str] = strawberry.field(default_factory=str)
    password: Optional[str] = strawberry.field(default_factory=str)
    dob: Optional[str] = strawberry.field(default_factory=str)
    phone_number: Optional[str] = strawberry.field(default_factory=str)
    address: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class ResponseUser:
    data: User | None
    err: str | None


@strawberry.type
class ResponseGetallUser:
    data: list[User] | None
    err: str | None
