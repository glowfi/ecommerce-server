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
    rating: float
    total_reviews: int
    images: list[list[str]]
    on_sale: bool
    price: float
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
    sellerID: str
    stock: int
    title: str
    rating: float
    total_reviews: int


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
    stock: Optional[int] = strawberry.field(default_factory=int)
    title: Optional[str] = strawberry.field(default_factory=str)
    rating: Optional[float] = strawberry.field(default_factory=float)
    total_reviews: int


@strawberry.type
class ResponseProduct:
    data: Product | None
    err: str | None


@strawberry.type
class ResponseGetallProduct:
    data: list[Product] | None
    err: str | None


@strawberry.type
class SearchResponse:
    brand: str
    categoryName: str
    description: str
    id: str
    price: float
    score: float
    paginationToken: str
    sellerName: str
    title: str
    coverImage: list[str]
    discount_percent: float
    stock: int
    rating: float


@strawberry.type
class SearchResponseResult:
    data: list[SearchResponse] | None
    lastToken: str | None
    err: str | None
