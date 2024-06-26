import asyncio
from beanie import DeleteRules
import strawberry
from Middleware.jwtbearer import IsAuthenticated
from models.dbschema import Reviews, User, Product
from Graphql.schema.reviews import (
    ResponseReviews as rre,
    InputReviews as ipre,
    InputUpdateReviews as ipure,
)
from helper.utils import encode_input, retval
import requests
import random
import os
from dotenv import find_dotenv, load_dotenv
import urllib.parse
from better_profanity import profanity


# Load dotenv
load_dotenv(find_dotenv(".env"))
RANDOMMER_KEY = os.getenv("RANDOMMER_KEY")
STAGE = os.getenv("STAGE")


async def delete_review(reviewID):
    get_rev = await Reviews.get(reviewID, fetch_links=True)
    await get_rev.delete(link_rule=DeleteRules.DELETE_LINKS)


async def update_product_rating(productID):
    pipeline = [
        {"$match": {"productId": productID}},
        {
            "$group": {
                "_id": None,
                "average_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1},
            }
        },
    ]
    getData = await Reviews.aggregate(aggregation_pipeline=pipeline).to_list()

    # Find Product
    prod = await Product.get(productID)

    if getData and getData[0].get("average_rating", ""):
        avgReviews = getData[0].get("average_rating")
        totalReviews = getData[0].get("total_reviews")

        await prod.update(
            {"$set": {"rating": avgReviews, "total_reviews": totalReviews}}
        )


async def insert_one_review(product, allUsers):
    productName = product.title
    productName = productName[: min(len(productName) - 1, 50)]
    quantity = 500

    params = {"quantity": quantity, "product": productName}
    query_string = urllib.parse.urlencode(params, doseq=True)

    data = requests.post(
        f"https://randommer.io/api/Text/Review?{query_string}",
        headers={"X-Api-Key": RANDOMMER_KEY},
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
                "rating": random.randint(1, 5),
            }
        )
        await new_rev.insert()


@strawberry.type
class Mutation:

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def generate_review(self) -> str:
        try:

            allUsers = await User.find_many().to_list()
            allProducts = await Product.find_many().to_list()

            tasks = [insert_one_review(product, allUsers) for product in allProducts]
            await asyncio.gather(*tasks)

            tasks = [update_product_rating(str(product.id)) for product in allProducts]
            await asyncio.gather(*tasks)

            return "Done"
        except Exception as e:
            return str(e)

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_review(self, data: ipre, info: strawberry.Info) -> rre:
        try:
            encoded_data = encode_input(data.__dict__)
            # Find User
            user = await User.get(
                encoded_data["userID"], fetch_links=True, nesting_depth=1
            )
            if user:
                # Find product
                prod = await Product.get(
                    encoded_data["productID"], fetch_links=True, nesting_depth=1
                )
                if prod:
                    profanity.load_censor_words()
                    encoded_data["comment"] = profanity.censor(encoded_data["comment"])
                    new_rev = Reviews(
                        **{
                            "comment": encoded_data["comment"],
                            "user_reviewed": user,
                            "product_reviewed": prod,
                            "userId": str(encoded_data["userID"]),
                            "productId": str(encoded_data["productID"]),
                            "rating": int(encoded_data["rating"]),
                        }
                    )
                    rev_ins = await new_rev.insert()

                    info.context["background_tasks"].add_task(
                        update_product_rating,
                        str(encoded_data["productID"]),
                    )

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

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
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

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_review(self, reviewID: str, info: strawberry.Info) -> rre:
        try:
            get_rev = await Reviews.get(reviewID)
            if get_rev:
                info.context["background_tasks"].add_task(delete_review, reviewID)
                return rre(data=get_rev, err=None)
            else:
                return rre(data=None, err=f"No review with reviewID {reviewID}")
        except Exception as e:
            return rre(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_review_by_id(self, reviewID: str) -> rre:
        try:
            get_rev = await Reviews.get(reviewID)
            if get_rev:
                return rre(data=get_rev, err=None)
            else:
                return rre(data=None, err=f"No review with reviewID {reviewID}")
        except Exception as e:
            return rre(data=None, err=str(e))
