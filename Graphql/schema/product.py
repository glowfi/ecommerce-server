import strawberry
from typing import TYPE_CHECKING, Annotated, Optional, Union

if TYPE_CHECKING:
    from .seller import Seller
    from .category import Category
    from .orders import Orders
    from .wishlist import Wishlist
    from .reviews import Reviews


@strawberry.type
class Product:
    id: str
    brand: str
    category: Union[Annotated["Category", strawberry.lazy(".category")], None]
    categoryName: str
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
    seller: Union[Annotated["Seller", strawberry.lazy(".seller")], None]
    sellerName: str
    stock: int
    title: str
    quantity: Union[int, None]
    wishedBy: Optional[list[Annotated["Wishlist", strawberry.lazy(".wishlist")]]] = (
        strawberry.field(default_factory=list)
    )
    orderedBy: Optional[list[Annotated["Orders", strawberry.lazy(".orders")]]] = (
        strawberry.field(default_factory=list)
    )
    reviewedBy: Optional[list[Annotated["Reviews", strawberry.lazy(".reviews")]]] = (
        strawberry.field(default_factory=list)
    )


@strawberry.input
class InputProduct:
    brand: str
    categoryID: str
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
    sellerID: str
    stock: int
    title: str


@strawberry.input
class InputUpdateProduct:
    brand: Optional[str] = strawberry.field(default_factory=str)
    coverImage: Optional[list[str]] = strawberry.field(default_factory=list)
    date_created: Optional[int] = strawberry.field(default_factory=int)
    date_created_human: Optional[str] = strawberry.field(default_factory=str)
    description: Optional[str] = strawberry.field(default_factory=str)
    discount_percent: Optional[float] = strawberry.field(default_factory=float)
    images: Optional[list[list[str]]] = strawberry.field(default_factory=list)
    on_sale: Optional[bool] = strawberry.field(default_factory=bool)
    price: Optional[float] = strawberry.field(default_factory=float)
    price_inr: Optional[float] = strawberry.field(default_factory=float)
    rating: Optional[int] = strawberry.field(default_factory=int)
    stock: Optional[int] = strawberry.field(default_factory=int)
    title: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class ResponseProduct:
    data: Product | None
    err: str | None


@strawberry.type
class ResponseGetallProduct:
    data: list[Product] | None
    err: str | None
