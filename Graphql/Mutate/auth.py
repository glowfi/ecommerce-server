import strawberry
from Graphql.schema.auth import InputLogin, Login, LoginResponse, LogoutResponse
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
    async def logout(self, userID: str, info: strawberry.Info) -> LogoutResponse:
        try:
            # Get redis object
            redis = info.context["redis_client"]
            await redis.delete(userID)

            return LogoutResponse(data="Logout", err=None)
        except Exception as e:
            return LogoutResponse(data=None, err=str(e))

    @strawberry.mutation
    async def login(self, data: InputLogin, info: strawberry.Info) -> LoginResponse:
        if data.userType.lower() not in ["admin", "seller", "user"]:
            return LoginResponse(
                data=None, err="userType mut be admin or seller or user"
            )

        else:
            checkUser = await checkUserExists(data.email, data.userType)
            if not checkUser:
                return LoginResponse(
                    data=None,
                    err=f"No such user with email {data.email} exists as {data.userType}",
                )

            elif not checkUser[0].confirmed:
                return LoginResponse(
                    data=None, err=f"Verify your account before logging in!"
                )

            elif checkUser[0].password != data.password:
                return LoginResponse(data=None, err=f"Wrong Password entered!")

            else:
                # Generate Token
                detail = {
                    "userID": str(checkUser[0].id),
                    "email": data.email,
                    "profile_pic": checkUser[0].profile_pic,
                    "name": checkUser[0].name,
                    "userType": data.userType,
                }
                accToken = await JWTManager.generate_token(detail)
                detail["accToken"] = accToken
                refToken = await JWTManager.generate_token(
                    detail, REFRESH_TOKEN_EXPIRE_MINUTES
                )

                userID = str(checkUser[0].id)
                res = info.context["response"]

                # Add reftoken to redis for currentUser
                redis = info.context["redis_client"]
                await redis.set(
                    userID,
                    refToken,
                    ex=(int(REFRESH_TOKEN_EXPIRE_MINUTES) * 60),
                )

                res.headers["Authorization"] = accToken
                # res.set_cookie(
                #     "refreshToken", refToken, httponly=True, samesite="strict"
                # )

                details = Login(
                    **{
                        **detail,
                        "address": checkUser[0].address,
                        "phone_number": checkUser[0].phone_number,
                    }
                )
                return LoginResponse(data=details, err=None)
