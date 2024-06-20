import os
from dotenv import load_dotenv, find_dotenv
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
from helper.forget_password_html import html_content_forget_password

# Load dotenv
load_dotenv(find_dotenv(".env"))
OTP_TOKEN_EXPIRE_MINUTES = os.getenv("OTP_TOKEN_EXPIRE_MINUTES")
STORE_NAME = " ".join(os.getenv("STORE_NAME").split("-"))
FRONTEND_URL = os.getenv("FRONTEND_URL")


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

            # Get email template
            html_content = (
                html_content_forget_password.replace("{{name}}", str(user[0].name))
                .replace(
                    "{{action_url_1}}", f"{FRONTEND_URL}/auth/resetpassword/{token}"
                )
                .replace("[Product Name]", str(STORE_NAME))
                .replace("{{operating_system}}", data.os)
                .replace("{{browser_name}}", data.browser)
                .replace("{{support_url}}", "")
                .replace("[Company Name, LLC]", f"{STORE_NAME} LLC")
            )

            # Send email
            info.context["background_tasks"].add_task(
                send_mail,
                {
                    "to": [data.email],
                    "subject": "Forgot Password Link",
                    "body": html_content,
                },
            )

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
