import strawberry
from Graphql.schema.orders import ResponseGetallOrders as rgor
from models.dbschema import Orders


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_orders() -> rgor:
        try:
            allOrders = await Orders.find_many(fetch_links=True).to_list()
            return rgor(data=allOrders, err=None)
        except Exception as e:
            return rgor(data=None, err=str(e))
