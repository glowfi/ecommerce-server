import strawberry
from Graphql.schema.wishlist import ResponseGetallWishlist as rgwi
from models.dbschema import Wishlist


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_wishlis() -> rgwi:
        try:
            allWishlist = await Wishlist.find_many(fetch_links=True).to_list()
            return rgwi(data=allWishlist, err=None)
        except Exception as e:
            return rgwi(data=None, err=str(e))
