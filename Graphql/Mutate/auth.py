import strawberry
from Graphql.schema.auth import InputLogin, Login, LoginResponse
from Middleware.jwtmanager import JWTManager
from dotenv import find_dotenv, load_dotenv
import os

from helper.utils import checkUserExists


# Load dotenv
load_dotenv(find_dotenv(".env"))
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def login(self, data: InputLogin, info: strawberry.Info) -> LoginResponse:
        if data.userType.lower() not in ["admin", "seller", "user"]:
            return LoginResponse(
                data=None, err="userType mut be admin or seller or user"
            )

        else:
            res = await checkUserExists(data.email, data.userType)
            if not res:
                return LoginResponse(
                    data=None,
                    err=f"No such user with email {data.email} exists as {data.userType}",
                )

            elif not res[0].confirmed:
                return LoginResponse(
                    data=None, err=f"Verify your account before logging in!"
                )

            elif res[0].password != data.password:
                return LoginResponse(data=None, err=f"Wrong Password entered!")

            else:
                # Generate Token
                detail = {
                    "userID": str(res[0].id),
                    "email": data.email,
                    "profile_pic": res[0].profile_pic,
                    "name": res[0].name,
                    "userType": data.userType,
                }
                accToken = await JWTManager.generate_token(detail)
                detail["accToken"] = accToken
                refToken = await JWTManager.generate_token(
                    detail, REFRESH_TOKEN_EXPIRE_MINUTES
                )
                res = info.context["response"]
                redis = info.context["redis_client"]
                await redis.set("accToken", accToken)
                res.headers["Authorization"] = accToken
                res.set_cookie(
                    "refreshToken", refToken, httponly=True, samesite="strict"
                )

                details = Login(**detail)
                return LoginResponse(data=details, err=None)
