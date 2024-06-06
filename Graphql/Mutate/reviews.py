import json
import strawberry
from models.dbschema import Reviews, User, Product
from Graphql.schema.reviews import (
    ResponseReviews as rre,
    InputReviews as ipre,
    InputUpdateReviews as ipure,
)
from helper.utils import encode_input
import requests
import random


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def generate_review(self) -> str:
        try:

            key = "7f0636b70f53464f8eb8ca81c74a8e9e"
            allUsers = await User.find_many(fetch_links=True).to_list()
            allProducts = await Product.find_many(fetch_links=True).to_list()

            print(len(allUsers))
            print(len(allProducts))

            for product in allProducts:
                productName = product.title
                quantity = 10

                data = requests.post(
                    f"https://randommer.io/api/Text/Review?quantity={quantity}&product={productName}",
                    headers={"X-Api-Key": key},
                ).json()

                for review in data:
                    randomUserIdx = random.randint(0, len(allUsers) - 1)
                    currUser = allUsers[randomUserIdx]
                    new_rev = Reviews(
                        **{
                            "comment": review,
                            "user_reviewed": currUser,
                            "product_reviewed": product,
                            "userId": str(currUser.id),
                            "productId": str(product.id),
                        }
                    )
                    await new_rev.insert()

            return "Done"
        except Exception as e:
            return str(e)

    @strawberry.mutation
    async def create_review(self, data: ipre) -> rre:
        try:
            encoded_data = encode_input(data.__dict__)
            print(encoded_data)
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
                            "userId": str(encoded_data["userID"]),
                            "productId": str(encoded_data["productID"]),
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
    async def update_review(self, data: ipure, reviewID: str) -> rre:
        try:
            encoded_data = encode_input(data.__dict__)
            get_rev = await Reviews.get(reviewID)
            if get_rev:
                rev_updated = await get_rev.update({"$set": encoded_data})
                return rre(data=rev_updated, err=None)
            else:
                return rre(data=None, err=f"No review with reviewID {reviewID}")
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
