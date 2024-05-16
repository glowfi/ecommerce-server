import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Wishlist:
    id: str
    user_wished: Annotated["User", strawberry.lazy(".user")]
    product_wished: Annotated["Product", strawberry.lazy(".product")]
    wishedAt: datetime
