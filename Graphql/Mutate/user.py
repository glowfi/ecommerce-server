import os
import strawberry
from Middleware.jwtmanager import JWTManager
from helper.sendmail import send_mail
from helper.utils import encode_input, get_pics
from models.dbschema import User
from Graphql.schema.user import (
    ResponseUser as ru,
    InputUser as ipu,
    InputUpdateUser as ipuu,
)
import json
from dotenv import load_dotenv, find_dotenv
from helper.confirm_email import html_content_confirm_email
import asyncio

# Load dotenv
load_dotenv(find_dotenv(".env"))
OTP_TOKEN_EXPIRE_MINUTES = os.getenv("OTP_TOKEN_EXPIRE_MINUTES")
STORE_NAME = os.getenv("STORE_NAME")
FRONTEND_URL = os.getenv("FRONTEND_URL")


async def insert_one_user(user):
    data = {**user, "confirmed": True}
    new_user = User(**data)
    await new_user.insert()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_users_from_dataset() -> str:
        with open("./dataset/user.json") as fp:
            data = json.load(fp)

        tasks = [insert_one_user(user) for user in data]
        await asyncio.gather(*tasks)

        return "Done!"

    @strawberry.mutation
    async def create_user(self, data: ipu, info: strawberry.Info) -> ru:
        try:
            encoded_data = encode_input(data.__dict__)
            encoded_data["profile_pic"] = get_pics(encoded_data["name"])
            new_user = User(**encoded_data)
            user_ins = await new_user.insert()

            # Generate Token
            userID = str(new_user.id)
            token = await JWTManager.generate_token(
                {"user_ID": userID}, str(OTP_TOKEN_EXPIRE_MINUTES)
            )

            # Get email template
            html_content = (
                html_content_confirm_email.replace("{{name}}", str(new_user.name))
                .replace("{{action_url}}", f"{FRONTEND_URL}/auth/verifyaccount/{token}")
                .replace("[Product Name]", str(STORE_NAME))
                .replace("{{support_url}}", "")
                .replace("[Company Name, LLC]", f"{STORE_NAME} LLC")
            )

            # Send email
            info.context["background_tasks"].add_task(
                send_mail,
                {
                    "to": [encoded_data["email"]],
                    "subject": "Account Confirmation",
                    "body": html_content,
                },
            )

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
