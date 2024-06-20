import strawberry
from Graphql.schema.wishlist import ResponseGetallWishlist as rgwi
from models.dbschema import Wishlist
import os
from dotenv import find_dotenv, load_dotenv
from Middleware.jwtbearer import IsAuthenticated
from helper.utils import retval


# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_all_wishlis() -> rgwi:
        try:
            allWishlist = await Wishlist.find_many(fetch_links=True).to_list()
            return rgwi(data=allWishlist, err=None)
        except Exception as e:
            return rgwi(data=None, err=str(e))
