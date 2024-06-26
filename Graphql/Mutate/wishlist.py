import os
from beanie import DeleteRules
import strawberry
from models.dbschema import Wishlist, User, Product
from Graphql.schema.wishlist import (
    ResponseWishlist as rwi,
    InputWishlist as ipwi,
    # InputUpdateWishlist as ipuwi,
)
from helper.utils import encode_input, retval
from Middleware.jwtbearer import IsAuthenticated
from dotenv import load_dotenv, find_dotenv


# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


async def delete_wishlist(wishID):
    get_wish = await Wishlist.get(wishID, fetch_links=True)
    await get_wish.delete(link_rule=DeleteRules.DELETE_LINKS)


@strawberry.type
class Mutation:

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_wish(self, data: ipwi) -> rwi:
        try:
            encoded_data = encode_input(data.__dict__)
            # Find User
            user = await User.get(encoded_data["userID"], fetch_links=True)
            if user:
                # Find product
                prod = await Product.get(encoded_data["productID"], fetch_links=True)
                if prod:
                    new_wish = Wishlist(
                        **{
                            "user_wished": user,
                            "product_wished": prod,
                        }
                    )
                    wish_ins = await new_wish.insert()
                    return rwi(data=wish_ins, err=None)
                else:
                    return rwi(
                        data=None,
                        err=f"No product found with id {encoded_data['productID']}",
                    )
            else:
                return rwi(
                    data=None, err=f"No user found with id {encoded_data['userID']}"
                )

        except Exception as e:
            return rwi(data=None, err=str(e))

    # @strawberry.mutation
    # async def update_wish(self, data: ipuwi, wishID: str) -> rwi:
    #     try:
    #         encoded_data = encode_input(data.__dict__)
    #         get_wish = await Wishlist.get(wishID)
    #         if get_wish:
    #             wish_updated = await get_wish.update({"$set": encoded_data})
    #             return rwi(data=wish_updated, err=None)
    #         else:
    #             return rwi(data=None, err=f"No wish with wishID {wishID}")
    #     except Exception as e:
    #         return rwi(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_wish(self, wishID: str, info: strawberry.Info) -> rwi:
        try:
            get_wish = await Wishlist.get(wishID)
            if get_wish:
                info.context["background_tasks"].add_task(delete_wishlist, wishID)
                return rwi(data=get_wish, err=None)
            else:
                return rwi(data=None, err=f"No wish with wishID {wishID}")
        except Exception as e:
            return rwi(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_wish_by_id(self, wishID: str) -> rwi:
        try:
            get_wish = await Wishlist.get(wishID)
            if get_wish:
                return rwi(data=get_wish, err=None)
            else:
                return rwi(data=None, err=f"No wish with wishID {wishID}")
        except Exception as e:
            return rwi(data=None, err=str(e))
