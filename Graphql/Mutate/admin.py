import strawberry
from Graphql.schema.admin import ResponseAdmin as rad, InputAdmin as ipad
from Middleware.jwtbearer import IsAuthenticated
from models.dbschema import Admin
from helper.utils import encode_input, retval, validate_inputs
from helper.password import get_password_hash
from dotenv import find_dotenv, load_dotenv
import os


# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = str(os.getenv("STAGE"))
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def create_admin(self, data: ipad) -> rad:
        encoded_data = encode_input(data.__dict__)
        if not encoded_data["email"] or not encoded_data["password"]:
            return rad(data=None, err="Please provide a valid input")

        res = await validate_inputs(encoded_data["email"], encoded_data["password"])

        if not res[0]:
            return rad(data=None, err=res[1])
        else:
            encoded_data["password"] = get_password_hash(encoded_data["password"])
            new_admin = Admin(**encoded_data)
            ins_admin = await new_admin.insert()
            return rad(data=ins_admin, err=None)
