import strawberry
import json
from models.dbschema import Category


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_categories_from_dataset() -> str:
        with open("./dataset/dataset.json") as fp:
            data = json.load(fp)

        hmap = {}
        for prod in data:
            hmap[prod["categoryID"]] = {
                "name": f"{prod["category"]}",
                "image": prod["categoryImage"],
            }

        all = []

        for cat in hmap:
            name, image = hmap[cat]["name"], hmap[cat]["image"]
            all.append(Category(name=name, categoryImage=image))

        await Category.insert_many(all)

        return "Done"
