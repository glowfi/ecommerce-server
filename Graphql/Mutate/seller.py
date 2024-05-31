import strawberry
import json
from helper.utils import encode_input
from models.dbschema import Seller
from Graphql.schema.seller import (
    ResponseSeller as rse,
    InputSeller as ipse,
    InputUpdateSeller as ipuse,
)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_sellers_from_dataset() -> str:
        with open("./dataset/dataset.json") as fp:
            data = json.load(fp)

        all = []
        for prod in data:
            all.append(Seller(**prod["seller_info"]))

        await Seller.insert_many(all)

        return "Done!"

    @strawberry.mutation
    async def create_seller(self, data: ipse) -> rse:
        try:
            encoded_data = encode_input(data.__dict__)
            new_seller = Seller(**encoded_data)
            seller_ins = await new_seller.insert()
            return rse(data=seller_ins, err=None)

        except Exception as e:
            return rse(data=None, err=str(e))

    @strawberry.mutation
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

    @strawberry.mutation
    async def delete_seller(self, sellerID: str) -> rse:
        try:
            get_seller = await Seller.get(sellerID)
            if get_seller:
                seller_deleted = await get_seller.delete()
                return rse(data=seller_deleted, err=None)
            else:
                return rse(data=None, err=f"No seller with sellerID {sellerID}")
        except Exception as e:
            return rse(data=None, err=str(e))

    @strawberry.mutation
    async def get_seller_by_id(self, sellerID: str) -> rse:
        try:
            get_seller = await Seller.get(sellerID)
            if get_seller:
                return rse(data=get_seller, err=None)
            else:
                return rse(data=None, err=f"No seller with sellerID {sellerID}")
        except Exception as e:
            return rse(data=None, err=str(e))
