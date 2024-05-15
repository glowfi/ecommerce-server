import strawberry
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .product import Product


@strawberry.type
class Seller:
    email: str
    phone_number: str
    dob: str
    password: str
    company_name: str
    company_address: str
    country: str
    seller_name: str
    products_selling: list[Annotated["Product", strawberry.lazy(".product")]]
