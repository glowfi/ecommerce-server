import strawberry
from models.dbschema import Wishlist, User, Product
from Graphql.schema.wishlist import (
    ResponseWishlist as rwi,
    InputWishlist as ipwi,
    # InputUpdateWishlist as ipuwi,
)
from helper.utils import encode_input


@strawberry.type
class Mutation:

    @strawberry.mutation
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

    @strawberry.mutation
    async def delete_wish(self, wishID: str) -> rwi:
        try:
            get_wish = await Wishlist.get(wishID)
            if get_wish:
                wish_deleted = await get_wish.delete()
                return rwi(data=wish_deleted, err=None)
            else:
                return rwi(data=None, err=f"No wish with wishID {wishID}")
        except Exception as e:
            return rwi(data=None, err=str(e))

    @strawberry.mutation
    async def get_wish_by_id(self, wishID: str) -> rwi:
        try:
            get_wish = await Wishlist.get(wishID)
            if get_wish:
                return rwi(data=get_wish, err=None)
            else:
                return rwi(data=None, err=f"No wish with wishID {wishID}")
        except Exception as e:
            return rwi(data=None, err=str(e))
