import strawberry

from Graphql.schema.resetpassword import (
    InputresetPassword,
    resetPassword,
    resetPasswordResponse as rpres,
)
from helper.utils import encode_input
from models.dbschema import User, OTP


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def reset_password(
        self,
        data: InputresetPassword,
    ) -> rpres:
        try:
            encoded_data = encode_input(data.__dict__)

            if encoded_data["token"] == "fromacc":
                get_user = await User.get(encoded_data["userid"], fetch_links=True)
                if not get_user:
                    return rpres(
                        data=None, err=f"No user with userid {encoded_data['userid']}!"
                    )
                else:
                    return rpres(
                        data=resetPassword(
                            userid=encoded_data["userid"], token=encoded_data["token"]
                        ),
                        err=None,
                    )

            else:
                # Update OTP Expired
                otp = await OTP.find_one(OTP.token == encoded_data["token"])

                if not otp or otp.hasExpired:
                    return rpres(data=None, err="Something wrong occured!")
                else:
                    USER_ID = otp.userID
                    get_user = await User.get(USER_ID, fetch_links=True)

                    if get_user:
                        otp.hasExpired = True
                        await otp.save()

                        # Get User
                        del encoded_data["token"]
                        await get_user.update({"$set": encoded_data})

                        return rpres(
                            data=resetPassword(
                                userid=USER_ID, token=data.__dict__["token"]
                            ),
                            err=None,
                        )
                    else:
                        return rpres(
                            data=None, err=f"No user with userID {encoded_data['id']}"
                        )
        except Exception as e:
            return rpres(data=None, err=str(e))
