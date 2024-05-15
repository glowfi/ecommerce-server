import strawberry
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .product import Product


@strawberry.type
class Category:
    name: str
    categoryImage: list[str]
    products_belonging: list[Annotated["Product", strawberry.lazy(".product")]]
