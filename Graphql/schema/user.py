import strawberry

from typing import TYPE_CHECKING, Annotated, Optional, Union

if TYPE_CHECKING:
    from .orders import Orders
    from .wishlist import Wishlist
    from .reviews import Reviews


@strawberry.type
class Address:
    street_address: str
    city: str
    state: str
    country: str
    countryCode: str
    zip_code: str


@strawberry.input
class AddressInput:
    street_address: Optional[str] = strawberry.field(default_factory=str)
    city: Optional[str] = strawberry.field(default_factory=str)
    country: Optional[str] = strawberry.field(default_factory=str)
    countryCode: Optional[str] = strawberry.field(default_factory=str)
    state: Optional[str] = strawberry.field(default_factory=str)
    zip_code: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class User:
    id: str
    email: str
    confirmed: bool
    profile_pic: Union[str, None]
    name: str
    password: str
    dob: str
    phone_number: str
    address: Address
    wishlist: list[Annotated["Wishlist", strawberry.lazy(".wishlist")]]
    orders: list[Annotated["Orders", strawberry.lazy(".orders")]]
    reviews: list[Annotated["Reviews", strawberry.lazy(".reviews")]]


@strawberry.input
class InputUser:
    email: str
    profile_pic: Optional[str] = strawberry.field(default_factory=str)
    name: str
    password: str
    dob: Optional[str] = strawberry.field(default_factory=str)
    phone_number: Optional[str] = strawberry.field(default_factory=str)
    address: Optional[AddressInput] = strawberry.field(default_factory=dict)


@strawberry.input
class InputUpdateUser:
    profile_pic: Optional[str] = strawberry.field(default_factory=str)
    email: Optional[str] = strawberry.field(default_factory=str)
    name: Optional[str] = strawberry.field(default_factory=str)
    password: Optional[str] = strawberry.field(default_factory=str)
    dob: Optional[str] = strawberry.field(default_factory=str)
    phone_number: Optional[str] = strawberry.field(default_factory=str)
    address: Optional[AddressInput] = strawberry.field(default_factory=str)


@strawberry.type
class ResponseUser:
    data: User | None
    err: str | None


@strawberry.type
class ResponseGetallUser:
    data: list[User] | None
    err: str | None
