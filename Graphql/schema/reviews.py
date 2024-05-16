import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Reviews:
    id: str
    user_reviewed: Annotated["User", strawberry.lazy(".user")]
    product_reviewed: Annotated["Product", strawberry.lazy(".product")]
    reviewedAt: datetime
