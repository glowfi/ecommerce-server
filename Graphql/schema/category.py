import strawberry
from typing import TYPE_CHECKING, Annotated, Optional

if TYPE_CHECKING:
    from .product import Product


@strawberry.type
class Category:
    id: str
    name: str
    categoryImage: list[str]
    products_belonging: list[Annotated["Product", strawberry.lazy(".product")]]


@strawberry.input
class InputCategory:
    name: str
    categoryImage: list[str]


@strawberry.input
class InputUpdateCategory:
    name: Optional[str]
    categoryImage: Optional[list[str]]


@strawberry.type
class ResponseCategory:
    data: Category | None
    err: str | None


@strawberry.type
class ResponseGetallCategory:
    data: list[Category] | None
    err: str | None
