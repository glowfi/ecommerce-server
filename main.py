from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.connection import beanie_connection
import strawberry
from Graphql.mutation import Mutation
from Graphql.query import Query
from strawberry.fastapi import GraphQLRouter
import uvicorn


# Lifespan startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect with beanie
    await beanie_connection.connect()

    yield

    # Close beanie connection
    await beanie_connection.disconnect()


# FastAPI app
app = FastAPI(
    title="Ecommerce", description="Fast API", version="1.0.0", lifespan=lifespan
)


# Default test router
@app.get("/")
def home():
    return "welcome home!"


# Add graphql endpoint
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, graphql_ide="apollo-sandbox")
app.include_router(graphql_app, prefix="/graphql")


# Start uvicorn server
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
