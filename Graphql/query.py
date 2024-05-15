from typing import List
import strawberry
from Graphql.schema.seller import Seller
import json
from models.dbschema import Seller as sl


@strawberry.type
class Query:
    @strawberry.field
    async def hello() -> str:
        return "hello"

    @strawberry.field()
    async def sellerTest() -> List[Seller] | None:
        return await sl.find_all(fetch_links=True).to_list()
