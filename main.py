from contextlib import asynccontextmanager
import os
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Depends
from config.connection import beanie_connection
from Redis.connection import redis_connection
import strawberry
from Graphql.mutation import Mutation
from Graphql.query import Query
from strawberry.fastapi import GraphQLRouter
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Read dotenv
load_dotenv(find_dotenv(".env"))
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Redis Client string
redis_client = {"client": None}


# Custom ctx_getter
def custom_context_dependency() -> dict:
    return redis_client


async def get_context(
    custom_value=Depends(custom_context_dependency),
):
    return {
        "redis_client": custom_value["client"],
    }


# Lifespan startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect with beanie and redis
    await beanie_connection.connect()
    await redis_connection.connect()
    redis_client["client"] = redis_connection.client

    yield

    # Close beanie and redis connection
    await beanie_connection.disconnect()
    await redis_connection.disconnect()


# FastAPI app
app = FastAPI(
    title="Ecommerce", description="Fast API", version="1.0.0", lifespan=lifespan
)

# Cors
origins = [
    str(FRONTEND_URL),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Default test router
@app.get("/")
def home():
    return "welcome home!"


# Add graphql endpoint
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema, graphql_ide="apollo-sandbox", context_getter=get_context
)
app.include_router(graphql_app, prefix="/graphql")


# Start uvicorn server
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
