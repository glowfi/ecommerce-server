import strawberry
import json
from models.dbschema import Product, Category, Seller
from Graphql.schema.product import (
    Product as pr,
    InputProduct as ipr,
    ResponseProduct as rpr,
    InputUpdateProduct as iupr,
)
from helper.utils import encode_input


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_products_from_dataset() -> str:
        with open("./dataset/dataset.json") as fp:
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

    @strawberry.mutation
    async def insert_product(self, data: ipr) -> rpr:
        try:
            encode_data = encode_input(data.__dict__)
            # Find Seller
            seller = await Seller.get(encode_data["sellerID"], fetch_links=True)
            # Find Category
            if seller:
                cat = await Category.get(encode_data["categoryID"], fetch_links=True)
                if cat:
                    encode_data["category"] = cat
                    encode_data["seller"] = seller

                    new_prod = Product(**encode_data)
                    prod_ins = await new_prod.insert()

                    return rpr(data=prod_ins, err=None)
                else:
                    return rpr(
                        data=None,
                        err=f"No category found with categoryID {encode_data["categoryID"]}",
                    )
            else:
                return rpr(
                    data=None,
                    err=f"No such seller with sellerID {encode_data["sellerID"]}",
                )
        except Exception as e:
            return rpr(data=None, err=str(e))

    @strawberry.mutation
    async def update_product(self, data: iupr) -> rpr:
        try:
            encode_data = encode_input(data.__dict__)
            # Find Seller
            seller = await Seller.get(encode_data["sellerID"], fetch_links=True)
            # Find Category
            if seller:
                cat = await Category.get(encode_data["categoryID"], fetch_links=True)
                if cat:
                    # Find Product
                    prod = await Product.get(encode_data["productID"], fetch_links=True)
                    if prod:
                        prod_updated = await prod.update({"$set": encode_data})
                        return rpr(data=prod_updated, err=None)
                    else:
                        return rpr(
                            data=None,
                            err=f"No product found with productID {encode_data["productID"]}",
                        )

                else:
                    return rpr(
                        data=None,
                        err=f"No category found with categoryID {encode_data["categoryID"]}",
                    )
            else:
                return rpr(
                    data=None,
                    err=f"No such seller with sellerID {encode_data["sellerID"]}",
                )

        except Exception as e:
            raise e

    @strawberry.mutation
    async def delete_product(self, productID: str) -> rpr:
        try:
            prod = await Product.get(productID, fetch_links=True)
            if prod:
                prod_delete = await prod.delete()
                return rpr(data=prod_delete, err=None)
            else:
                return rpr(
                    data=None, err=f"No product found with productID {productID}"
                )
        except Exception as e:
            return rpr(data=None, err=str(e))

    @strawberry.mutation
    async def get_product_by_id(self, productID: str) -> rpr:
        try:
            prod = await Product.get(productID, fetch_links=True)
            if prod:
                return rpr(data=prod, err=None)
            else:
                return rpr(
                    data=None, err=f"No product found with productID {productID}"
                )
        except Exception as e:
            return rpr(data=None, err=str(e))
