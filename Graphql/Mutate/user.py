import os
from beanie import DeleteRules
from bson import ObjectId
import strawberry
from Middleware.jwtmanager import JWTManager
from helper.utils import encode_input, get_pics, retval
from models.dbschema import User
from Graphql.schema.user import (
    ResponseUser as ru,
    InputUser as ipu,
    InputUpdateUser as ipuu,
)
import json
from dotenv import load_dotenv, find_dotenv
import asyncio
from helper.password import get_password_hash
from Middleware.jwtbearer import IsAuthenticated


# Load dotenv
load_dotenv(find_dotenv(".env"))
OTP_TOKEN_EXPIRE_MINUTES = os.getenv("OTP_TOKEN_EXPIRE_MINUTES")
STORE_NAME = " ".join(os.getenv("STORE_NAME").split("-"))
FRONTEND_URL = os.getenv("FRONTEND_URL")
STAGE = os.getenv("STAGE")
KAFKA_MAIL_TOPIC = os.getenv("KAFKA_MAIL_TOPIC")


async def insert_one_user(user):
    data = {**user, "confirmed": True}
    new_user = User(**data)
    await new_user.insert()


async def delete_user_account(userID, producer):
    get_user = await User.find_one(
        User.id == ObjectId(userID), fetch_links=True, nesting_depth=1
    )
    await get_user.delete(link_rule=DeleteRules.DELETE_LINKS)

    produce_data = {
        "STORE_NAME": STORE_NAME,
        "name": get_user.name,
        "email": get_user.email,
    }

    # Publish message to apache kafka topic to send mail
    final_data = {"operation": "close_account", "data": produce_data}
    await producer.send(KAFKA_MAIL_TOPIC, json.dumps(final_data).encode())


@strawberry.type
class Mutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
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
            get_user = await User.find_one(User.email == encoded_data["email"])
            if get_user:
                return ru(data=None, err="Email already used!")
            else:
                encoded_data["profile_pic"] = get_pics(encoded_data["name"])
                encoded_data["password"] = get_password_hash(encoded_data["password"])
                encoded_data["name"] = encoded_data["name"].title()
                new_user = User(**encoded_data)
                user_ins = await new_user.insert()

                # Generate Token
                userID = str(new_user.id)
                token = await JWTManager.generate_token(
                    {"user_ID": userID}, str(OTP_TOKEN_EXPIRE_MINUTES)
                )

                # Format Data to be produced
                produce_data = {
                    "FRONTEND_URL": str(FRONTEND_URL),
                    "new_user": str(new_user.name),
                    "STORE_NAME": STORE_NAME,
                    "email": encoded_data["email"],
                    "token": token,
                }
                final_data = {"operation": "confirm_email", "data": produce_data}

                print(f"{FRONTEND_URL}/auth/verifyaccount/{token}")

                # Publish message to apache kafka topic to send mail
                producer = info.context["kafka_producer"]
                await producer.send(KAFKA_MAIL_TOPIC, json.dumps(final_data).encode())

                return ru(data=user_ins, err=None)

        except Exception as e:
            return ru(data=None, err=str(e))

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
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

    @strawberry.mutation(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def delete_user(self, userID: str, info: strawberry.Info) -> ru:
        try:
            get_user = await User.find_one(
                User.id == ObjectId(userID), fetch_links=True, nesting_depth=1
            )
            if get_user:

                # Get producer
                producer = info.context["kafka_producer"]
                info.context["background_tasks"].add_task(
                    delete_user_account, userID, producer
                )
                return ru(data=get_user, err=None)
            else:
                return ru(data=None, err=f"No user with userID {userID}")
        except Exception as e:
            return ru(data=None, err=str(e))

    @strawberry.mutation(
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
