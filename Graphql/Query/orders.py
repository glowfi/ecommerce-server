import strawberry
from Graphql.schema.orders import ResponseGetallOrders as rgor, Orders as orde
from models.dbschema import Orders, User
from Middleware.jwtbearer import IsAuthenticated
import os
from dotenv import find_dotenv, load_dotenv
from helper.utils import retval


# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_all_orders() -> rgor:
        try:
            allOrders = await Orders.find_many(fetch_links=True).to_list()
            return rgor(data=allOrders, err=None)
        except Exception as e:
            return rgor(data=None, err=str(e))

    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_orders_by_userid(
        self, userID: str, skipping: int, limit: int
    ) -> rgor:
        try:

            # getUser = await User.get(userID)

            # # print(getUser, "User")

            # getOrders = await Orders.aggregate(
            #     aggregation_pipeline=[
            #         {"$match": {"userid": userID}},
            #         {"$sort": {"_id": -1}},
            #         {"$skip": skipping},
            #         {"$limit": limit},
            #     ]
            # ).to_list()

            # # print(getOrders)

            # data = []

            # for dic in getOrders:
            #     tmp = {}
            #     tmp = {**dic}
            #     tmp["id"] = str(tmp["_id"])[:]

            #     tmp["user_ordered"] = getUser

            #     tmp1 = {}
            #     for key, val in tmp["address"].items():
            #         tmp1[key] = val

            #     tmp["address"] = tmp1

            #     del tmp["_id"]
            #     data.append(orde(**tmp))

            # print(data[0].address.keys(), type(data[0].address))

            allOrders = (
                await Orders.find(Orders.userid == userID, fetch_links=True)
                .sort(-Orders.id)
                .skip(skipping)
                .limit(limit)
                .to_list()
            )

            return rgor(data=allOrders, err=None)
            # return rgor(data=data, err=None)
        except Exception as e:
            return rgor(data=None, err=str(e))
