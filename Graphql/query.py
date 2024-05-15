import strawberry
from Graphql.Query.seller import Query as sellerQuery


@strawberry.type
class Query(sellerQuery):
    @strawberry.field
    async def hello() -> str:
        return "hello"
