from beanie import Document, Link, BackLink, Indexed
from datetime import datetime
from pydantic import Field


class User(Document):
    email: Indexed(str, unique=True)
    name: str
    password: str
    dob: str
    phone_number: str
    address: str
    wishlist: list[BackLink["Wishlist"]] = Field(
        original_field="user_wished", default_factory=list
    )
    orders: list[BackLink["Orders"]] = Field(
        original_field="user_ordered", default_factory=list
    )
    reviews: list[BackLink["Reviews"]] = Field(
        original_field="user_reviewd", default_factory=list
    )


class Admin(Document):
    email: Indexed(str, unique=True)
    password: str


class Seller(Document):
    email: Indexed(str, unique=True)
    phone_number: str
    dob: str
    password: str
    company_name: str
    company_address: str
    country: str
    seller_name: str
    products_selling: list[BackLink["Product"]] = Field(
        original_field="seller", default_factory=list
    )


class Category(Document):
    name: str
    categoryImage: list[str]
    products_belonging: list[BackLink["Product"]] = Field(
        original_field="category", default_factory=list
    )


class Product(Document):
    brand: str
    category: Link[Category]
    coverImage: list[str]
    date_created: int
    date_created_human: str
    description: str
    discount_percent: float
    images: list[list[str]]
    on_sale: bool = Field(default=False)
    price: float
    price_inr: float
    rating: int
    seller: Link[Seller]
    stock: int
    title: str
    wishedBy: list[BackLink["Wishlist"]] = Field(
        original_field="product_wished", default_factory=list
    )
    orderedBy: list[BackLink["Orders"]] = Field(
        original_field="product_ordered", default_factory=list
    )
    reviewedBy: list[BackLink["Reviews"]] = Field(
        original_field="product_reviewed", default_factory=list
    )


class Wishlist(Document):
    user_wished: Link["User"]
    product_wished: Link["Product"]
    wishedAt: datetime = Field(default=datetime.now())


class Orders(Document):
    user_ordered: Link["User"]
    product_ordered: Link["Product"]
    orderedAt: datetime = Field(default=datetime.now())


class Reviews(Document):
    user_reviewd: Link["User"]
    product_reviewed: Link["Product"]
    orderedAt: datetime = Field(default=datetime.now())
