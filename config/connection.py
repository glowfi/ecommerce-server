import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import find_dotenv, load_dotenv

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
            document_models=[],
        )

    async def disconnect(self):
        print("Beanie Disconnected!")


beanie_connection = BeanieConnection()
