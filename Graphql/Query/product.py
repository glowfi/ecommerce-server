import strawberry
from Graphql.schema.product import ResponseGetallProduct as rgpr
from models.dbschema import Product


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_products() -> rgpr:
        try:
            allProducts = await Product.find_many(fetch_links=True, limit=10).to_list()
            return rgpr(data=allProducts, err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))
