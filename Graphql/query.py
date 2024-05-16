import strawberry
from Graphql.Query.seller import Query as sellerQuery
from Graphql.Query.product import Query as productQuery


@strawberry.type
class Query(sellerQuery, productQuery):
    @strawberry.field
    async def hello() -> str:
        return "hello"
