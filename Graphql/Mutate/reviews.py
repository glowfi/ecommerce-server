import strawberry
from models.dbschema import Reviews, User, Product
from Graphql.schema.reviews import (
    ResponseReviews as rre,
    InputReviews as ipre,
    InputUpdateReviews as ipure,
)
from helper.utils import encode_input


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_review(self, data: ipre) -> rre:
        try:
            encoded_data = encode_input(data.__dict__)
            # Find User
            user = await User.get(encoded_data["userID"], fetch_links=True)
            if user:
                # Find product
                prod = await Product.get(encoded_data["productID"], fetch_links=True)
                if prod:
                    new_rev = Reviews(
                        **{
                            "comment": encoded_data["comment"],
                            "user_reviewed": user,
                            "product_reviewed": prod,
                        }
                    )
                    rev_ins = await new_rev.insert()
                    return rre(data=rev_ins, err=None)
                else:
                    return rre(
                        data=None,
                        err=f"No product found with id {encoded_data['productID']}",
                    )
            else:
                return rre(
                    data=None, err=f"No user found with id {encoded_data['userID']}"
                )

        except Exception as e:
            return rre(data=None, err=str(e))

    @strawberry.mutation
    async def update_review(self, data: ipure) -> rre:
        try:
            encoded_data = encode_input(data.__dict__)
            get_rev = await Reviews.get(encoded_data["reviewID"])
            if get_rev:
                rev_updated = await get_rev.update({"$set": encoded_data})
                return rre(data=rev_updated, err=None)
            else:
                return rre(
                    data=None, err=f"No review with reviewID {encoded_data['reviewID']}"
                )
        except Exception as e:
            return rre(data=None, err=str(e))

    @strawberry.mutation
    async def delete_review(self, reviewID: str) -> rre:
        try:
            get_rev = await Reviews.get(reviewID)
            if get_rev:
                rev_deleted = await get_rev.delete()
                return rre(data=rev_deleted, err=None)
            else:
                return rre(data=None, err=f"No review with reviewID {reviewID}")
        except Exception as e:
            return rre(data=None, err=str(e))

    @strawberry.mutation
    async def get_review_by_id(self, reviewID: str) -> rre:
        try:
            get_rev = await Reviews.get(reviewID)
            if get_rev:
                return rre(data=get_rev, err=None)
            else:
                return rre(data=None, err=f"No review with reviewID {reviewID}")
        except Exception as e:
            return rre(data=None, err=str(e))
