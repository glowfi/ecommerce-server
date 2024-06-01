import strawberry
from Graphql.schema.confirmaccount import ConfirmAccount
from Middleware.jwtmanager import JWTManager
from models.dbschema import User


@strawberry.type
class Query:
    @strawberry.field
    async def confirm_account(self, token: str) -> ConfirmAccount:

        try:
            # Get token data
            data = await JWTManager.get_token_data(token)

            if data is None:
                return ConfirmAccount(data=None, err="Expired")
            else:
                get_user = await User.get(data["user_ID"])
                if get_user.confirmed:
                    return ConfirmAccount(data="Verified", err=None)

                # Update user confirmation account
                get_user.confirmed = True
                await get_user.save()

                return ConfirmAccount(data="Verified", err=None)

        except Exception as e:
            return ConfirmAccount(data=None, err=str(e))
