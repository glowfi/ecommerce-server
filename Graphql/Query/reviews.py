import strawberry
from Graphql.schema.reviews import ResponseGetallReviews as rgrev
from models.dbschema import Product, Reviews, User


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
                getReviews = await Reviews.find_many(
                    Reviews.userId == userID,
                    fetch_links=True,
                    skip=skipping,
                    limit=limit,
                ).to_list()
                return rgrev(data=getReviews, err=None)
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
            ).to_list()

            ans = []

            for review in getReviews:
                ans.append(review)

            return rgrev(data=ans, err=None)
        except Exception as e:
            return rgrev(data=None, err=str(e))
