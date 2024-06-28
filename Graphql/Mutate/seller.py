from beanie import DeleteRules
import strawberry
import json
from helper.password import get_password_hash
from helper.utils import encode_input, retval
from models.dbschema import Seller
from Graphql.schema.seller import (
    ResponseSeller as rse,
    InputSeller as ipse,
    InputUpdateSeller as ipuse,
)
from dotenv import find_dotenv, load_dotenv
import os
from Middleware.jwtbearer import IsAuthenticated


# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


async def delete_seller(sellerID):
    get_seller = await Seller.get(sellerID, fetch_links=True)
    await get_seller.delete(link_rule=DeleteRules.DELETE_LINKS)


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def insert_sellers_from_dataset() -> str:
        with open("./dataset/dataset.json") as fp:
            data = json.load(fp)

        all = []
        for prod in data:
            data = {**prod["seller_info"]}
            all.append(Seller(**data))

        await Seller.insert_many(all)

        return "Done!"

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_seller(self, data: ipse) -> rse:
        try:
            encoded_data = encode_input(data.__dict__)
            encoded_data["password"] = get_password_hash(encoded_data["password"])
            new_seller = Seller(**encoded_data)
            seller_ins = await new_seller.insert()
            return rse(data=seller_ins, err=None)

        except Exception as e:
            return rse(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def update_seller(self, data: ipuse, sellerID: str) -> rse:
        try:
            encoded_data = encode_input(data.__dict__)
            get_seller = await Seller.get(sellerID)
            if get_seller:
                seller_updated = await get_seller.update({"$set": encoded_data})
                return rse(data=seller_updated, err=None)
            else:
                return rse(data=None, err=f"No seller with sellerID {sellerID}")
        except Exception as e:
            return rse(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_seller(self, sellerID: str, info: strawberry.Info) -> rse:
        try:
            get_seller = await Seller.get(sellerID)
            if get_seller:
                info.context["background_tasks"].add_task(delete_seller, sellerID)
                return rse(data=get_seller, err=None)
            else:
                return rse(data=None, err=f"No seller with sellerID {sellerID}")
        except Exception as e:
            return rse(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_seller_by_id(self, sellerID: str) -> rse:
        try:
            get_seller = await Seller.get(sellerID)
            if get_seller:
                return rse(data=get_seller, err=None)
            else:
                return rse(data=None, err=f"No seller with sellerID {sellerID}")
        except Exception as e:
            return rse(data=None, err=str(e))
