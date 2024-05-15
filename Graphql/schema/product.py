import strawberry
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .seller import Seller
    from .category import Category
    from .orders import Orders
    from .wishlist import Wishlist
    from .reviews import Reviews


@strawberry.type
class Product:
    brand: str
    category: Annotated["Category", strawberry.lazy(".category")]
    coverImage: list[str]
    date_created: int
    date_created_human: str
    description: str
    discount_percent: float
    images: list[list[str]]
    on_sale: bool
    price: float
    price_inr: float
    rating: int
    seller: Annotated["Seller", strawberry.lazy(".seller")]
    stock: int
    title: str
    wishedBy: list[Annotated["Wishlist", strawberry.lazy(".wishlist")]]
    orderedBy: list[Annotated["Orders", strawberry.lazy(".orders")]]
    reviewedBy: list[Annotated["Reviews", strawberry.lazy(".reviews")]]
