import strawberry
from Graphql.schema.product import ResponseGetallProduct as rgpr
from models.dbschema import Product


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_products() -> rgpr:
        try:
            allProducts = await Product.find_many(fetch_links=True).to_list()
            return rgpr(data=allProducts, err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))

    @strawberry.field
    async def get_all_products_paginate(self, skipping: int, limit: int) -> rgpr:
        try:
            allProducts = await Product.find_many(
                fetch_links=True, skip=skipping, limit=limit
            ).to_list()
            return rgpr(data=allProducts, err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))

    @strawberry.field
    async def get_products_by_search_term(self, term: str) -> rgpr:
        try:
            allProducts = await Product.find_many(fetch_links=True).to_list()
            final = []
            for product in allProducts:
                currProduct = product.__dict__
                if (
                    term.lower() in currProduct["title"].lower()
                    or term.lower() in currProduct["description"].lower()
                    or term.lower() in currProduct["category"].__dict__["name"].lower()
                    or term.lower() in currProduct["brand"].lower()
                    or term.lower()
                    in currProduct["seller"].__dict__["seller_name"].lower()
                ):
                    final.append(product)
            return rgpr(data=final, err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))
