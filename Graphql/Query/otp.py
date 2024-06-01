import strawberry
from helper.utils import encode_input
from models.dbschema import OTP
from Graphql.schema.otp import OTPInput, OTPResponse as otpres, OTP as otp_obj


@strawberry.type
class Query:
    @strawberry.field
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
