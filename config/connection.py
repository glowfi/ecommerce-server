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
import httpx


# Load dotenv
load_dotenv(find_dotenv(".env"))

# Mongodb database and collection
MONGODB_COLLECTION = "Product"
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

# Atlas API related
ATLAS_API_BASE_URL = "https://cloud.mongodb.com/api/atlas/v1.0"
ATLAS_PROJECT_ID = os.getenv("MONGODB_ALTAS_PROJECT_ID")
ATLAS_CLUSTER_NAME = os.getenv("MONGODB_ALTAS_CLUSTER")
ATLAS_CLUSTER_API_URL = (
    f"{ATLAS_API_BASE_URL}/groups/{ATLAS_PROJECT_ID}/clusters/{ATLAS_CLUSTER_NAME}"
)
ATLAS_SEARCH_INDEX_API_URL = f"{ATLAS_CLUSTER_API_URL}/fts/indexes"
ATLAS_API_PUBLIC_KEY = os.getenv("MONGODB_ALTAS_PUBLIC_KEY")
ATLAS_API_PRIVATE_KEY = os.getenv("MONGODB_ALTAS_PRIVATE_KEY")

# Indexes
USER_SEARCH_INDEX_NAME = os.getenv("USER_SEARCH_INDEX_NAME")
USER_AUTOCOMPLETE_INDEX_NAME = os.getenv("USER_AUTOCOMPLETE_INDEX_NAME")


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

    async def findIndexByName(self, indexName: str):
        URL = f"{ATLAS_SEARCH_INDEX_API_URL}/{MONGODB_DATABASE}/{MONGODB_COLLECTION}"

        try:
            async with httpx.AsyncClient() as client:
                auth = httpx.DigestAuth(
                    username=str(ATLAS_API_PUBLIC_KEY),
                    password=str(ATLAS_API_PRIVATE_KEY),
                )
                r = await client.get(URL, auth=auth)
                print(r.status_code)

                res = []
                for indexex in r.json():
                    for index_prop in indexex:
                        if indexex[index_prop] == indexName:
                            res.append(indexName)
                return res
        except Exception as e:
            print(str(e))
            return []

    async def upsertSearchIndex(self):
        userSearchIndex = await self.findIndexByName(str(USER_SEARCH_INDEX_NAME))
        if not userSearchIndex:
            async with httpx.AsyncClient() as client:
                auth = httpx.DigestAuth(
                    username=str(ATLAS_API_PUBLIC_KEY),
                    password=str(ATLAS_API_PRIVATE_KEY),
                )
                r = await client.post(
                    f"https://cloud.mongodb.com/api/atlas/v2/groups/{ATLAS_PROJECT_ID}/clusters/{ATLAS_CLUSTER_NAME}/search/indexes?pretty=true",
                    json={
                        "collectionName": MONGODB_COLLECTION,
                        "database": MONGODB_DATABASE,
                        "definition": {
                            "mappings": {
                                "dynamic": True,
                                "fields": {
                                    "sellerName": {
                                        "type": "string",
                                        "analyzer": "lucene.standard",
                                    },
                                    "description": {
                                        "type": "string",
                                        "analyzer": "lucene.standard",
                                    },
                                    "brand": {
                                        "type": "string",
                                        "analyzer": "lucene.standard",
                                    },
                                    "categoryName": {
                                        "type": "string",
                                        "analyzer": "lucene.standard",
                                    },
                                    "title": {
                                        "type": "string",
                                        "analyzer": "lucene.standard",
                                    },
                                },
                            }
                        },
                        "name": USER_SEARCH_INDEX_NAME,
                    },
                    auth=auth,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/vnd.atlas.2024-05-30+json",
                    },
                )
                print(r.status_code)
                print(r.json())

        else:
            print("Not Creating indexes because index already exist!")

    async def disconnect(self):
        print("Beanie Disconnected!")


beanie_connection = BeanieConnection()
