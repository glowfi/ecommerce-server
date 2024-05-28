import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import find_dotenv, load_dotenv
from models.dbschema import (
    OTP,
    User,
    Admin,
    Seller,
    Category,
    Product,
    Orders,
    Reviews,
    Wishlist,
)


# Load dotenv
load_dotenv(find_dotenv(".env"))


# BeanieConnection
class BeanieConnection:
    def __init__(self):
        self.DB_URL = os.getenv("DATABASE_URL")

    async def connect(self):
        client = AsyncIOMotorClient(self.DB_URL)
        db = client["ecommerce"]
        print("Beanie Connected!", self.DB_URL)

        await init_beanie(
            database=db,
            document_models=[
                User,
                Admin,
                Seller,
                Category,
                Product,
                Orders,
                Reviews,
                Wishlist,
                OTP,
            ],
        )

    async def disconnect(self):
        print("Beanie Disconnected!")


beanie_connection = BeanieConnection()
