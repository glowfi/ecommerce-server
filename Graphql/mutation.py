import strawberry
import json
from models.dbschema import Category, Seller, Product
import time


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def hello() -> str:
        return "hello"

    @strawberry.mutation
    async def insert_categories_from_dataset() -> str:
        with open("./dataset.json") as fp:
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

    @strawberry.mutation
    async def insert_sellers_from_dataset() -> str:
        with open("./dataset.json") as fp:
            data = json.load(fp)

        all = []
        for prod in data:
            all.append(Seller(**prod["seller_info"]))

        await Seller.insert_many(all)

        return "Done!"

    @strawberry.mutation
    async def insert_products_from_dataset() -> str:
        with open("./dataset.json") as fp:
            data = json.load(fp)

        all = []
        c_ins = 0
        # c_sold=0

        for prod in data:
            # Find Seller
            seller = await Seller.find(
                Seller.email == prod["seller_info"]["email"], fetch_links=True
            ).first_or_none()

            # if seller.products_selling:
            #     c_ins += 1

            # Find Category
            if seller:
                cat = await Category.find(
                    Category.name == prod["category"], fetch_links=True
                ).first_or_none()
                if c_ins % 25 == 0:
                    time.sleep(6)
                if cat:
                    c_ins += 1
                    # print(cat)
                    # all.append(
                    new_prod = Product(
                        brand=prod["brand"],
                        category=cat,
                        coverImage=prod["coverImage"],
                        date_created=prod["date_created"],
                        date_created_human=prod["date_created_human"],
                        description=prod["description"],
                        discount_percent=prod["discount_percent"],
                        images=prod["images"],
                        price=prod["price"],
                        price_inr=prod["price_inr"],
                        rating=prod["rating"],
                        seller=seller,
                        stock=prod["stock"],
                        title=prod["title"],
                    )
                    await new_prod.insert()
                    # )
            # if all:
            #     await Product.insert_many(all)

        print(c_ins)

        # Insert all products
        return ""
