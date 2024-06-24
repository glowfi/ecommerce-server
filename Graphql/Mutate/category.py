import strawberry
from beanie import DeleteRules
import json
from Middleware.jwtbearer import IsAuthenticated
from models.dbschema import Category
from Graphql.schema.category import (
    ResponseCategory as rca,
    InputCategory as ipca,
    InputUpdateCategory as ipuca,
)
from helper.utils import encode_input, retval
from dotenv import find_dotenv, load_dotenv
import os

# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = str(os.getenv("STAGE"))


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def insert_categories_from_dataset(self) -> str:
        with open("./dataset/dataset.json") as fp:
            data = json.load(fp)

        hmap = {}
        for prod in data:
            hmap[prod["categoryID"]] = {
                "name": f"{prod['category']}",
                "image": prod["categoryImage"],
            }

        all = []

        for cat in hmap:
            name, image = hmap[cat]["name"], hmap[cat]["image"]
            all.append(Category(name=name, categoryImage=image))

        await Category.insert_many(all)

        return "Done"

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_category(self, data: ipca) -> rca:
        try:
            encode_data = encode_input(data.__dict__)
            new_cat = Category(**encode_data)
            cat_ins = await new_cat.insert()
            return rca(data=cat_ins, err=None)
        except Exception as e:
            return rca(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def update_category(self, data: ipuca, categoryID: str) -> rca:
        try:
            encode_data = encode_input(data.__dict__)
            get_cat = await Category.get(categoryID, fetch_links=True)
            if get_cat:
                cat_updated = await get_cat.update({"$set": encode_data})
                return rca(data=cat_updated, err=None)
            else:
                return rca(
                    data=None,
                    err=f"No Category found with categoryID {categoryID}",
                )
        except Exception as e:
            return rca(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_category(self, categoryID: str) -> rca:
        try:
            get_cat = await Category.get(categoryID, fetch_links=True)
            if get_cat:
                cat_delete = await get_cat.delete(link_rule=DeleteRules.DELETE_LINKS)
                return rca(data=cat_delete, err=None)
            else:
                return rca(
                    data=None,
                    err=f"No Category found with categoryID {categoryID}",
                )
        except Exception as e:
            return rca(data=None, err=str(e))

    @strawberry.mutation
    async def get_category_by_id(self, categoryID: str) -> rca:
        try:
            get_cat = await Category.get(categoryID, fetch_links=True)
            if get_cat:
                return rca(data=get_cat, err=None)
            else:
                return rca(
                    data=None,
                    err=f"No Category found with categoryID {categoryID}",
                )
        except Exception as e:
            return rca(data=None, err=str(e))
