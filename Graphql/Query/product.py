from typing import Union
import strawberry
from Graphql.schema.product import (
    ResponseGetallProduct as rgpr,
    SearchResponse,
    SearchResponseResult,
)
from models.dbschema import Product
from Graphql.schema.product import (
    ResponseProduct as rpr,
)
from dotenv import load_dotenv, find_dotenv
import os

# Load dotenv
load_dotenv(find_dotenv(".env"))

TOP_RESULTS = int(os.getenv("TOP_RESULTS_SEARCH"))
USER_SEARCH_INDEX_NAME = os.getenv("USER_SEARCH_INDEX_NAME")


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
            allProducts = await Product.find_many(skip=skipping, limit=limit).to_list()
            return rgpr(data=allProducts, err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))

    @strawberry.field
    async def get_products_by_search_term_atlas_search(
        self, term: str, limit: int, lastTokensaved: str
    ) -> SearchResponseResult:
        try:
            if lastTokensaved:
                data = await Product.aggregate(
                    aggregation_pipeline=[
                        {
                            "$search": {
                                "index": USER_SEARCH_INDEX_NAME,
                                "text": {
                                    "query": term,
                                    "path": [
                                        "brand",
                                        "description",
                                        "categoryName",
                                        "sellerName",
                                        "title",
                                    ],
                                    "fuzzy": {},
                                },
                                "sort": {
                                    "score": {"$meta": "searchScore"},
                                },
                                "searchAfter": lastTokensaved,
                            },
                        },
                        {"$limit": limit},
                        {
                            "$project": {
                                "_id": 1,
                                "score": {"$meta": "searchScore"},
                                "paginationToken": {"$meta": "searchSequenceToken"},
                                "sellerName": 1,
                                "brand": 1,
                                "description": 1,
                                "categoryName": 1,
                                "coverImage": 1,
                                "title": 1,
                                "price": 1,
                                "rating": 1,
                            },
                        },
                    ]
                ).to_list()
            else:
                data = await Product.aggregate(
                    aggregation_pipeline=[
                        {
                            "$search": {
                                "index": USER_SEARCH_INDEX_NAME,
                                "text": {
                                    "query": term,
                                    "path": [
                                        "brand",
                                        "description",
                                        "categoryName",
                                        "sellerName",
                                        "title",
                                    ],
                                    "fuzzy": {},
                                },
                                "sort": {
                                    "score": {"$meta": "searchScore"},
                                },
                            },
                        },
                        {"$limit": limit},
                        {
                            "$project": {
                                "_id": 1,
                                "score": {"$meta": "searchScore"},
                                "paginationToken": {"$meta": "searchSequenceToken"},
                                "sellerName": 1,
                                "brand": 1,
                                "description": 1,
                                "categoryName": 1,
                                "coverImage": 1,
                                "title": 1,
                                "price": 1,
                                "rating": 1,
                            },
                        },
                    ]
                ).to_list()
            final_data = []

            for dic in data:
                tmp = {}
                tmp = {**dic}
                tmp["id"] = str(tmp["_id"])[:]

                del tmp["_id"]
                final_data.append(SearchResponse(**tmp))

            return SearchResponseResult(
                data=final_data,
                lastToken=final_data[-1].paginationToken if final_data else "",
                err=None,
            )
        except Exception as e:
            return SearchResponseResult(data=None, lastToken=None, err=str(e))

    @strawberry.field
    async def get_products_by_search_term(self, term: str) -> rgpr:
        try:
            allProducts = await Product.find_many().to_list()
            final = []
            for product in allProducts:
                currProduct = product.__dict__
                if (
                    term.lower() in currProduct["title"].lower()
                    or term.lower() in currProduct["description"].lower()
                    or term.lower() in currProduct["categoryName"].lower()
                    or term.lower() in currProduct["brand"].lower()
                    or term.lower() in currProduct["sellerName"].lower()
                ):
                    final.append(product)
            return rgpr(data=final[: min(6, len(final))], err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))

    @strawberry.field
    async def get_products_by_search_term_paginate(
        self, term: str, skipping: int, limit: int
    ) -> rgpr:
        try:
            allProducts = await Product.find_many().to_list()
            final = []
            for product in allProducts:
                currProduct = product.__dict__
                if (
                    term.lower() in currProduct["title"].lower()
                    or term.lower() in currProduct["description"].lower()
                    or term.lower() in currProduct["categoryName"].lower()
                    or term.lower() in currProduct["brand"].lower()
                    or term.lower() in currProduct["sellerName"].lower()
                ):
                    final.append(product)

            paginated_final = []

            for i in range(skipping, len(final)):
                paginated_final.append(final[i])

            return rgpr(data=paginated_final[:limit], err=None)
        except Exception as e:
            return rgpr(data=None, err=str(e))

    @strawberry.field
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
