import os
from dotenv import load_dotenv, find_dotenv
import strawberry
from Graphql.schema.forgotpassword import (
    ForgotPassword,
    ForgotPasswordResponse,
    InputForgotPassword,
)
from Middleware.jwtmanager import JWTManager
from helper.utils import checkUserExists
from models.dbschema import OTP
import json

# Load dotenv
load_dotenv(find_dotenv(".env"))
OTP_TOKEN_EXPIRE_MINUTES = os.getenv("OTP_TOKEN_EXPIRE_MINUTES")
STORE_NAME = " ".join(os.getenv("STORE_NAME").split("-"))
FRONTEND_URL = os.getenv("FRONTEND_URL")
KAFKA_MAIL_TOPIC = os.getenv("KAFKA_MAIL_TOPIC")


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def forgot_password(
        self, data: InputForgotPassword, info: strawberry.Info
    ) -> ForgotPasswordResponse:

        # Check User exists
        user = await checkUserExists(data.email, data.userType)

        if not user:
            return ForgotPasswordResponse(data=None, err="No such user exists!")
        else:
            # Generate Token
            userID = str(user[0].id)
            token = await JWTManager.generate_token({}, str(OTP_TOKEN_EXPIRE_MINUTES))
            new_otp = OTP(userID=userID, token=token)
            await new_otp.insert()

            # Publish message to apache kafka topic to send mail
            producer = info.context["kafka_producer"]
            produce_data = {
                "FRONTEND_URL": FRONTEND_URL,
                "STORE_NAME": STORE_NAME,
                "os": data.os,
                "browser": data.browser,
                "name": str(user[0].name),
                "token": token,
                "email": data.email,
            }
            final_data = {"operation": "forgot_password", "data": produce_data}
            await producer.send(KAFKA_MAIL_TOPIC, json.dumps(final_data).encode())

            return ForgotPasswordResponse(
                data=ForgotPassword(
                    email=data.email,
                    userType=data.userType,
                    browser=data.browser,
                    os=data.os,
                    token=token,
                ),
                err=None,
            )
