import strawberry
from Graphql.schema.user import ResponseGetallUser as rgu, ResponseUser as ru
from models.dbschema import User
import os
from dotenv import find_dotenv, load_dotenv
from Middleware.jwtbearer import IsAuthenticated
from helper.utils import retval


# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_all_users() -> rgu:
        try:
            allUsers = await User.find_many(fetch_links=True, nesting_depth=1).to_list()
            return rgu(data=allUsers, err=None)
        except Exception as e:
            return rgu(data=None, err=str(e))

    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def get_user_by_id(self, userID: str) -> ru:
        try:
            get_user = await User.get(userID)
            if get_user:
                return ru(data=get_user, err=None)
            else:
                return ru(data=None, err=f"No user with userID {userID}")
        except Exception as e:
            return ru(data=None, err=str(e))
