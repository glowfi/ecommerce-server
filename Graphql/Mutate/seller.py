import strawberry
import json
from models.dbschema import Seller


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
