import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional

from Graphql.schema.user import AddressInput, InputUpdateUser

if TYPE_CHECKING:
    from .product import Product
    from .user import User


@strawberry.type
class Razorpay:
    razorpay_payment_id: Optional[str] = strawberry.field(default_factory=str)
    razorpay_order_id: Optional[str] = strawberry.field(default_factory=str)
    razorpay_signature: Optional[str] = strawberry.field(default_factory=str)


@strawberry.type
class Orders:
    id: str
    amount: float
    isPending: bool
    hasFailed: bool
    payment_by: str
    razorpay_details: Razorpay
    user_ordered: Annotated["User", strawberry.lazy(".user")]
    product_ordered: Annotated["Product", strawberry.lazy(".product")]
    orderedAt: datetime


@strawberry.input
class OrderUserDetails:
    address: AddressInput
    phone_number: str


@strawberry.input
class InputOrders:
    userDetails: OrderUserDetails
    amount: float
    userID: str
    productsOrdered: list[list[str]]
    payment_by: str


@strawberry.input
class RazorpayUpdate:
    razorpay_payment_id: Optional[str] = strawberry.field(default_factory=str)
    razorpay_order_id: Optional[str] = strawberry.field(default_factory=str)
    razorpay_signature: Optional[str] = strawberry.field(default_factory=str)


@strawberry.input
class InputUpdateOrders:
    orderID: str
    hasFailed: bool
    isPending: bool
    razorpay_details: RazorpayUpdate


@strawberry.type
class ResponseOrders:
    data: Orders | None
    err: str | None


@strawberry.type
class ResponseGetallOrders:
    data: list[Orders] | None
    err: str | None
