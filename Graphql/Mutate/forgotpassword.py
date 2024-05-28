import os
from dotenv import load_dotenv
from dotenv.main import find_dotenv
import strawberry
from Graphql.schema.forgotpassword import (
    ForgotPassword,
    ForgotPasswordResponse,
    InputForgotPassword,
)
from Middleware.jwtmanager import JWTManager
from helper.sendmail import send_mail
from helper.utils import checkUserExists, generate_random_number
from models.dbschema import OTP

# Load dotenv
load_dotenv(find_dotenv(".env"))
OTP_TOKEN_EXPIRE_MINUTES = os.getenv("OTP_TOKEN_EXPIRE_MINUTES")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")


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
            # Generate OTP
            otp = generate_random_number(10)
            userID = str(user[0].id)
            detail = {"OTP": otp}
            token = JWTManager.generate_token(detail, OTP_TOKEN_EXPIRE_MINUTES)
            new_otp = OTP(userID=userID, token=token)
            await new_otp.insert()

            # Send email
            # info.context["background_tasks"].add_task(
            #     send_mail,
            #     {
            #         "to": ["hoyinij401@hutov.com"],
            #         "subject": "Forgot Password Link",
            #         "body": f"OTP {otp}",
            #     },
            # )

            await send_mail(
                {
                    "to": ["hoyinij401@hutov.com"],
                    "subject": "Forgot Password Link",
                    "body": f"OTP {otp}",
                }
            )

            return ForgotPasswordResponse(
                data=ForgotPassword(email=data.email, userType=data.userType), err=None
            )
