import strawberry
from helper.utils import encode_input, retval
from models.dbschema import OTP
from Graphql.schema.otp import OTPInput, OTPResponse as otpres, OTP as otp_obj
from Middleware.jwtbearer import IsAuthenticated
import os
from dotenv import find_dotenv, load_dotenv

# Load dotenv
load_dotenv(find_dotenv(".env"))
STAGE = os.getenv("STAGE")


@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[IsAuthenticated if STAGE == "production" else retval]
    )
    async def check_otp_expired(self, data: OTPInput) -> otpres:

        encoded_data = encode_input(data.__dict__)

        # Update OTP Expired
        otp = await OTP.find_one(OTP.token == encoded_data["token"])

        if not otp:
            return otpres(data=None, err="Something wrong occured!")

        else:
            return otpres(
                data=otp_obj(
                    userID=otp.userID,
                    token=otp.token,
                    lastUsed=otp.lastUsed,
                    hasExpired=otp.hasExpired,
                ),
                err=None,
            )
