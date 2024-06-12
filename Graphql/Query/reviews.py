import strawberry
from Graphql.schema.reviews import ResponseGetallReviews as rgrev, Reviews as rv
from models.dbschema import Product, Reviews, User
import pymongo


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
    async def get_all_reviews_by_user_id(
        self, userID: str, skipping: int, limit: int
    ) -> rgrev:
        try:
            print(userID, skipping, limit)
            getProd = await User.get(userID)
            if getProd:
                data = (
                    await Reviews.find(Reviews.userId == userID, fetch_links=True)
                    .sort(-Reviews.id)
                    .skip(skipping)
                    .limit(limit)
                    .to_list()
                )

                #     getReviews = await Reviews.aggregate(
                #         aggregation_pipeline=[
                #             {"$match": {"userId": userID}},
                #             {"$sort": {"reviewedAt": -1}},
                #             {"$skip": skipping},
                #             {"$limit": limit},
                #         ]
                #     ).to_list()

                #     data = []

                #     for dic in getReviews:
                #         tmp = {}
                #         tmp = {**dic}
                #         tmp["id"] = str(tmp["_id"])[:]

                #         product = await Product.get(tmp["productId"])
                #         user = await User.get(tmp["userId"])

                #         tmp["user_reviewed"] = user
                #         tmp["product_reviewed"] = product

                #         del tmp["_id"]
                #         del tmp["orderedAt"]

                #         data.append(rv(**tmp))

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
