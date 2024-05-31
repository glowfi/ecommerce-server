import strawberry
from helper.utils import encode_input
from models.dbschema import User
from Graphql.schema.user import (
    ResponseUser as ru,
    InputUser as ipu,
    InputUpdateUser as ipuu,
)
import json


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_users_from_dataset() -> str:
        with open("./dataset/user.json") as fp:
            data = json.load(fp)

        for user in data:
            new_user = User(**user)
            await new_user.insert()

        return "Done!"

    @strawberry.mutation
    async def create_user(self, data: ipu) -> ru:
        try:
            encoded_data = encode_input(data.__dict__)
            new_user = User(**encoded_data)
            user_ins = await new_user.insert()
            return ru(data=user_ins, err=None)

        except Exception as e:
            return ru(data=None, err=str(e))

    @strawberry.mutation
    async def update_user(self, data: ipuu, userID: str) -> ru:
        try:
            encoded_data = encode_input(data.__dict__)
            get_user = await User.get(userID)
            if get_user:
                user_updated = await get_user.update({"$set": encoded_data})
                return ru(data=user_updated, err=None)
            else:
                return ru(data=None, err=f"No user with userID {userID}")
        except Exception as e:
            return ru(data=None, err=str(e))

    @strawberry.mutation
    async def delete_user(self, userID: str) -> ru:
        try:
            get_user = await User.get(userID)
            if get_user:
                user_deleted = await get_user.delete()
                return ru(data=user_deleted, err=None)
            else:
                return ru(data=None, err=f"No user with userID {userID}")
        except Exception as e:
            return ru(data=None, err=str(e))

    @strawberry.mutation
    async def get_user_by_id(self, userID: str) -> ru:
        try:
            get_user = await User.get(userID)
            if get_user:
                return ru(data=get_user, err=None)
            else:
                return ru(data=None, err=f"No user with userID {userID}")
        except Exception as e:
            return ru(data=None, err=str(e))
