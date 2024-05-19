import strawberry
from typing import TYPE_CHECKING, Annotated, Optional

if TYPE_CHECKING:
    from .product import Product


@strawberry.type
class Seller:
    id: str
    email: str
    phone_number: str
    dob: str
    password: str
    company_name: str
    company_address: str
    country: str
    seller_name: str
    products_selling: list[Annotated["Product", strawberry.lazy(".product")]]


@strawberry.input
class InputSeller:
    id: str
    email: str
    phone_number: str
    dob: str
    password: str
    company_name: str
    company_address: str
    country: str
    seller_name: str


@strawberry.input
class InputUpdateSeller:
    email: Optional[str] = strawberry.field(default_factory=str)
    phone_number: Optional[str] = strawberry.field(default_factory=str)
    dob: Optional[str] = strawberry.field(default_factory=str)
    password: Optional[str] = strawberry.field(default_factory=str)
    company_name: Optional[str] = strawberry.field(default_factory=str)
    company_address: Optional[str] = strawberry.field(default_factory=str)
    country: Optional[str] = strawberry.field(default_factory=str)
    seller_name: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class ResponseSeller:
    data: Seller | None
    err: str | None


@strawberry.type
class ResponseGetallSeller:
    data: list[Seller] | None
    err: str | None
