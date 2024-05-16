import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Orders:
    id: str
    user_ordered: Annotated["User", strawberry.lazy(".user")]
    product_ordered: Annotated["Product", strawberry.lazy(".product")]
    orderedAt: datetime
