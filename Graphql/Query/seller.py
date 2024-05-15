import strawberry
from Graphql.schema.seller import Seller
from models.dbschema import Seller as sl


@strawberry.type
class Query:
    @strawberry.field()
    async def sellerTest() -> list[Seller] | None:
        return await sl.find_all(fetch_links=True).to_list()
