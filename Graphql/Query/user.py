import strawberry
from Graphql.schema.user import ResponseGetallUser as rgu, ResponseUser as ru
from models.dbschema import User


@strawberry.type
class Query:
    @strawberry.field
    async def get_all_users() -> rgu:
        try:
            allUsers = await User.find_many(fetch_links=True).to_list()
            return rgu(data=allUsers, err=None)
        except Exception as e:
            return rgu(data=None, err=str(e))

    @strawberry.field
    async def get_user_by_id(self, userID: str) -> ru:
        try:
            get_user = await User.get(userID)
            if get_user:
                return ru(data=get_user, err=None)
            else:
                return ru(data=None, err=f"No user with userID {userID}")
        except Exception as e:
            return ru(data=None, err=str(e))
