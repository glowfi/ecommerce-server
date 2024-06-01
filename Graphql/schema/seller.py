import strawberry
from typing import TYPE_CHECKING, Annotated, Optional

from Graphql.schema.user import Address, AddressInput

if TYPE_CHECKING:
    from .product import Product


@strawberry.type
class Seller:
    id: str
    email: str
    phone_number: str
    confirmed: bool
    dob: str
    password: str
    company_name: str
    company_address: Address
    country: str
    seller_name: str
    profile_pic: str
    products_selling: list[Annotated["Product", strawberry.lazy(".product")]]


@strawberry.input
class InputSeller:
    id: str
    email: str
    phone_number: str
    dob: str
    password: str
    company_name: str
    company_address: AddressInput = strawberry.field(default_factory=dict)
    seller_name: str
    profile_pic: Optional[str] = strawberry.field(default_factory=str)


@strawberry.input
class InputUpdateSeller:
    email: Optional[str] = strawberry.field(default_factory=str)
    phone_number: Optional[str] = strawberry.field(default_factory=str)
    profile_pic: Optional[str] = strawberry.field(default_factory=str)
    dob: Optional[str] = strawberry.field(default_factory=str)
    password: Optional[str] = strawberry.field(default_factory=str)
    company_name: Optional[str] = strawberry.field(default_factory=str)
    company_address: Optional[AddressInput] = strawberry.field(default_factory=dict)
    seller_name: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class ResponseSeller:
    data: Seller | None
    err: str | None


@strawberry.type
class ResponseGetallSeller:
    data: list[Seller] | None
    err: str | None
