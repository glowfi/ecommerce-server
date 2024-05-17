import strawberry
from Graphql.schema.seller import ResponseGetallSeller as rgse
from models.dbschema import Seller


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_seller() -> rgse:
        try:
            allSellers = await Seller.find_many(fetch_links=True, limit=10).to_list()
            return rgse(data=allSellers, err=None)
        except Exception as e:
            return rgse(data=None, err=str(e))
