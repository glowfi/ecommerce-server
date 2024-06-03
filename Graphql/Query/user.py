import strawberry
from Graphql.schema.user import ResponseGetallUser as rgu
from models.dbschema import User


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_categories() -> rgu:
        try:
            allUsers = await User.find_many(fetch_links=True).to_list()
            return rgu(data=allUsers, err=None)
        except Exception as e:
            return rgu(data=None, err=str(e))
