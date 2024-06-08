import strawberry
from Graphql.schema.category import ResponseGetallCategory as rgca
from models.dbschema import Category


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_categories(self, info: strawberry.Info) -> rgca:

        try:
            allCategories = await Category.find_many().to_list()

            return rgca(data=allCategories, err=None)
        except Exception as e:
            return rgca(data=None, err=str(e))
