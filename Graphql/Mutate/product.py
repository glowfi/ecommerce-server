import strawberry
import json
from models.dbschema import Product, Category, Seller


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_products_from_dataset() -> str:
        with open("./dataset.json") as fp:
            data = json.load(fp)

        for prod in data:
            # Find Seller
            seller = await Seller.find(
                Seller.email == prod["seller_info"]["email"], fetch_links=True
            ).first_or_none()

            # Find Category
            if seller:
                cat = await Category.find(
                    Category.name == prod["category"], fetch_links=True
                ).first_or_none()
                if cat:
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
        return "Done!"
