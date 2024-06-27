import strawberry
from Graphql.schema.reviews import (
    ResponseGetallReviews as rgrev,
    Reviews as rv,
    ReviewsPercentage,
    ReviewsPercentageResponse,
)
from Middleware.jwtbearer import IsAuthenticated
from helper.utils import retval
from models.dbschema import Product, Reviews, User
from dotenv import load_dotenv, find_dotenv
import os

# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_reviews() -> rgrev:
        try:
            allReviews = await Reviews.find_many(fetch_links=True).to_list()
            return rgrev(data=allReviews, err=None)
        except Exception as e:
            return rgrev(data=None, err=str(e))

    @strawberry.field
    async def get_all_reviews_by_product_id(self, productID: str) -> rgrev:
        try:
            getProd = await Product.get(productID)
            if getProd:
                getReviews = await Reviews.find_many(
                    Reviews.productId == productID, fetch_links=True
                ).to_list()
                return rgrev(data=getReviews, err=None)
            else:
                return rgrev(data=None, err=f"No Proudct with {productID} exists!")

        except Exception as e:
            return rgrev(data=None, err=str(e))

    @strawberry.field
    async def get_reviews_percentage(self, prodID: str) -> ReviewsPercentageResponse:

        try:
            pipeline = [
                {"$match": {"productId": prodID}},
                {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
                {
                    "$group": {
                        "_id": None,
                        "totalReviews": {"$sum": "$count"},
                        "fiveStars": {
                            "$sum": {
                                "$cond": {
                                    "if": {"$eq": ["$_id", 5]},
                                    "then": "$count",
                                    "else": 0,
                                }
                            }
                        },
                        "fourStars": {
                            "$sum": {
                                "$cond": {
                                    "if": {"$eq": ["$_id", 4]},
                                    "then": "$count",
                                    "else": 0,
                                }
                            }
                        },
                        "threeStars": {
                            "$sum": {
                                "$cond": {
                                    "if": {"$eq": ["$_id", 3]},
                                    "then": "$count",
                                    "else": 0,
                                }
                            }
                        },
                        "twoStars": {
                            "$sum": {
                                "$cond": {
                                    "if": {"$eq": ["$_id", 2]},
                                    "then": "$count",
                                    "else": 0,
                                }
                            }
                        },
                        "oneStars": {
                            "$sum": {
                                "$cond": {
                                    "if": {"$eq": ["$_id", 1]},
                                    "then": "$count",
                                    "else": 0,
                                }
                            }
                        },
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "totalReviews": 1,
                        "fiveStars": {
                            "$multiply": [
                                {"$divide": ["$fiveStars", "$totalReviews"]},
                                100,
                            ]
                        },
                        "fourStars": {
                            "$multiply": [
                                {"$divide": ["$fourStars", "$totalReviews"]},
                                100,
                            ]
                        },
                        "threeStars": {
                            "$multiply": [
                                {"$divide": ["$threeStars", "$totalReviews"]},
                                100,
                            ]
                        },
                        "twoStars": {
                            "$multiply": [
                                {"$divide": ["$twoStars", "$totalReviews"]},
                                100,
                            ]
                        },
                        "oneStars": {
                            "$multiply": [
                                {"$divide": ["$oneStars", "$totalReviews"]},
                                100,
                            ]
                        },
                    }
                },
            ]
            getData = await Reviews.aggregate(aggregation_pipeline=pipeline).to_list()
            if getData:
                return ReviewsPercentageResponse(
                    data=ReviewsPercentage(**getData[0]), err=None
                )
            return ReviewsPercentageResponse(data=None, err=None)

        except Exception as e:
            return ReviewsPercentageResponse(data=None, err=str(e))

    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_all_reviews_by_user_id(
        self, userID: str, skipping: int, limit: int
    ) -> rgrev:
        try:
            getUser = await User.get(userID)
            if getUser:
                # data = (
                #     await Reviews.find(Reviews.userId == userID, fetch_links=True)
                #     .sort(-Reviews.id)
                #     .skip(skipping)
                #     .limit(limit)
                #     .to_list()
                # )

                getReviews = await Reviews.aggregate(
                    aggregation_pipeline=[
                        {"$match": {"userId": userID}},
                        {"$sort": {"_id": -1}},
                        {"$skip": skipping},
                        {"$limit": limit},
                    ]
                ).to_list()

                data = []

                for dic in getReviews:
                    tmp = {}
                    tmp = {**dic}
                    tmp["id"] = str(tmp["_id"])[:]

                    product = await Product.get(tmp["productId"])
                    # user = await User.get(tmp["userId"])

                    tmp["user_reviewed"] = getUser
                    tmp["product_reviewed"] = product

                    del tmp["_id"]

                    data.append(rv(**tmp))

                return rgrev(data=data, err=None)
            else:
                return rgrev(data=None, err=f"No User with {userID} exists!")

        except Exception as e:
            return rgrev(data=None, err=str(e))

    @strawberry.field
    async def get_reviews_paginate(
        self, prodID: str, skipping: int, limit: int
    ) -> rgrev:
        try:
            getReviews = await Reviews.find_many(
                Reviews.productId == prodID,
                fetch_links=True,
                nesting_depth=1,
                skip=skipping,
                limit=limit,
                sort=-Reviews.id,
            ).to_list()

            # ans = []

            # for review in getReviews:
            #     ans.append(review)

            return rgrev(data=getReviews, err=None)
        except Exception as e:
            return rgrev(data=None, err=str(e))
