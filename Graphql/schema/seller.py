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
    id: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    dob: Optional[str]
    password: Optional[str]
    company_name: Optional[str]
    company_address: Optional[str]
    country: Optional[str]
    seller_name: Optional[str]


@strawberry.type
class ResponseSeller:
    data: Seller | None
    err: str | None


@strawberry.type
class ResponseGetallSeller:
    data: list[Seller] | None
    err: str | None
