from beanie import Document, Link, BackLink, Indexed
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, Union


class Address(BaseModel):
    street_address: Optional[str] = Field(default_factory=str)
    city: Optional[str] = Field(default_factory=str)
    state: Optional[str] = Field(default_factory=str)
    country: Optional[str] = Field(default_factory=str)
    countryCode: Optional[str] = Field(default_factory=str)
    zip_code: Optional[int] = Field(default_factory=int)


class User(Document):
    email: Indexed(str, unique=True)
    name: str
    password: Optional[str] = Field(default_factory=str)
    dob: Optional[str] = Field(default_factory=str)
    phone_number: Optional[str] = Field(default_factory=str)
    address: Optional[Address] = Field(default_factory=Address)
    profile_pic: Optional[str] = Field(default_factory=str)
    confirmed: Optional[bool] = Field(default=False)
    wishlist: list[BackLink["Wishlist"]] = Field(
        json_schema_extra={"original_field": "user_wished"}, default_factory=list
    )
    orders: list[BackLink["Orders"]] = Field(
        json_schema_extra={"original_field": "user_ordered"}, default_factory=list
    )
    reviews: list[BackLink["Reviews"]] = Field(
        json_schema_extra={"original_field": "user_reviewed"}, default_factory=list
    )

    class Config:
        from_attributes = True


class Admin(Document):
    email: Indexed(str, unique=True)
    password: str

    class Config:
        from_attributes = True


class Seller(Document):
    email: Indexed(str, unique=True)
    phone_number: str
    confirmed: Optional[bool] = Field(default=False)
    dob: str
    password: str
    profile_pic: Optional[str] = Field(default_factory=str)
    company_name: str
    company_address: Optional[Address] = Field(default_factory=Address)
    seller_name: str
    products_selling: list[BackLink["Product"]] = Field(
        json_schema_extra={"original_field": "seller"}, default_factory=list
    )

    class Config:
        from_attributes = True


class Category(Document):
    name: str
    categoryImage: list[str]
    products_belonging: list[BackLink["Product"]] = Field(
        json_schema_extra={"original_field": "category"}, default_factory=list
    )

    class Config:
        from_attributes = True


class Product(Document):
    brand: str
    category: Link[Category]
    categoryName: str
    coverImage: list[str]
    date_created: int
    date_created_human: str
    description: str
    discount_percent: float
    rating: float = Field(default=0.0)
    total_reviews: int = Field(default=0)
    images: list[list[str]]
    on_sale: bool = Field(default=False)
    price: float
    seller: Link[Seller]
    sellerName: str
    stock: int
    title: str
    wishedBy: list[BackLink["Wishlist"]] = Field(
        json_schema_extra={"original_field": "product_wished"}, default_factory=list
    )
    # orderedBy: list[BackLink["Orders"]] = Field(
    #     json_schema_extra={"original_field": "products_ordered"}, default_factory=list
    # )
    reviewedBy: list[BackLink["Reviews"]] = Field(
        json_schema_extra={"original_field": "product_reviewed"}, default_factory=list
    )

    class Config:
        from_attributes = True


class Wishlist(Document):
    user_wished: Link["User"]
    product_wished: Link["Product"]
    wishedAt: datetime = Field(default=datetime.now())

    class Config:
        from_attributes = True


class Razorpay(BaseModel):
    razorpay_payment_id: Optional[str] = Field(default_factory=str)
    razorpay_order_id: Optional[str] = Field(default_factory=str)
    razorpay_signature: Optional[str] = Field(default_factory=str)


class Product_Ordered(Product):
    quantity: int


class Orders(Document):
    id: ObjectId = Field(default_factory=ObjectId)
    amount: float
    isPending: bool = Field(default=True)
    hasFailed: bool = Field(default=False)
    payment_by: str = Field(default_factory=str)
    razorpay_details: Razorpay = Field(default_factory=dict)
    user_ordered: Link["User"]
    userid: str
    products_ordered: list[Product_Ordered]
    orderedAt: datetime = Field(default=datetime.now())
    address: Optional[Address] = Field(default_factory=Address)
    name: str
    email: str
    phone_number: str
    update_address: bool
    shipping_fee: float
    tax: float

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class Reviews(Document):
    comment: str
    user_reviewed: Link["User"]
    product_reviewed: Link["Product"]
    rating: int
    userId: str
    productId: str
    reviewedAt: datetime = Field(default=datetime.now())

    class Config:
        from_attributes = True


class OTP(Document):
    userID: str
    token: str
    lastUsed: datetime = Field(default=datetime.now())
    hasExpired: bool = Field(default=False)

    class Config:
        from_attributes = True
