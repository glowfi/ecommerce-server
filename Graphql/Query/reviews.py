import strawberry
from Graphql.schema.reviews import ResponseGetallReviews as rgrev
from models.dbschema import Reviews


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_orders() -> rgrev:
        try:
            allReviews = await Reviews.find_many(fetch_links=True).to_list()
            return rgrev(data=allReviews, err=None)
        except Exception as e:
            return rgrev(data=None, err=str(e))
