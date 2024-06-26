from beanie import DeleteRules
import strawberry
import asyncio
import json
from models.dbschema import Product, Category, Seller
from Graphql.schema.product import (
    Product as pr,
    InputProduct as ipr,
    ResponseProduct as rpr,
    InputUpdateProduct as iupr,
)
from helper.utils import encode_input, retval
from dotenv import load_dotenv, find_dotenv
from Middleware.jwtbearer import IsAuthenticated
import os

# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = str(os.getenv("STAGE"))


async def delete_product(productID):
    prod = await Product.get(productID, fetch_links=True)
    await prod.delete(link_rule=DeleteRules.DELETE_LINKS)


async def insert_one_product(prod):
    # Find Seller
    seller = await Seller.find(
        Seller.email == prod["seller_info"]["email"], fetch_links=True, nesting_depth=1
    ).first_or_none()

    # Find Category
    if seller:
        cat = await Category.find(
            Category.name == prod["category"], fetch_links=True, nesting_depth=1
        ).first_or_none()
        if cat:
            new_prod = Product(
                brand=prod["brand"],
                category=cat,
                categoryName=cat.name,
                coverImage=prod["coverImage"],
                date_created=prod["date_created"],
                date_created_human=prod["date_created_human"],
                description=prod["description"],
                discount_percent=prod["discount_percent"],
                images=prod["images"],
                price=prod["price"],
                seller=seller,
                sellerName=seller.seller_name,
                stock=prod["stock"],
                title=prod["title"],
            )
            await new_prod.insert()


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def insert_products_from_dataset() -> str:
        with open("./dataset/dataset.json") as fp:
            data = json.load(fp)

        tasks = [insert_one_product(prod) for prod in data]
        await asyncio.gather(*tasks)
        return "Done!"

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def insert_product(self, data: ipr) -> rpr:
        try:
            encode_data = encode_input(data.__dict__)
            # Find Seller
            seller = await Seller.get(
                encode_data["sellerID"], fetch_links=True, nesting_depth=1
            )
            # Find Category
            if seller:
                cat = await Category.get(
                    encode_data["categoryID"], fetch_links=True, nesting_depth=1
                )
                if cat:
                    encode_data["category"] = cat
                    encode_data["seller"] = seller
                    encode_data["categoryName"] = cat.name
                    encode_data["sellerName"] = seller.seller_name

                    new_prod = Product(**encode_data)
                    prod_ins = await new_prod.insert()

                    return rpr(data=prod_ins, err=None)
                else:
                    return rpr(
                        data=None,
                        err=f"No category found with categoryID {encode_data['categoryID']}",
                    )
            else:
                return rpr(
                    data=None,
                    err=f"No such seller with sellerID {encode_data['sellerID']}",
                )
        except Exception as e:
            return rpr(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def update_product(self, data: iupr, productID: str) -> rpr:
        try:
            encode_data = encode_input(data.__dict__)
            # Find Product
            prod = await Product.get(productID, fetch_links=True, nesting_depth=1)
            if prod:
                prod_updated = await prod.update({"$set": encode_data})
                return rpr(data=prod_updated, err=None)
            else:
                return rpr(
                    data=None,
                    err=f"No product found with productID {productID}",
                )
        except Exception as e:
            return rpr(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_product(self, productID: str, info: strawberry.Info) -> rpr:
        try:
            prod = await Product.get(productID, fetch_links=True, nesting_depth=1)
            if prod:
                info.context["background_tasks"].add_task(delete_product, productID)
                return rpr(data=prod, err=None)
            else:
                return rpr(
                    data=None, err=f"No product found with productID {productID}"
                )
        except Exception as e:
            return rpr(data=None, err=str(e))
