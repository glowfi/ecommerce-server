import json
import typing
from strawberry.permission import BasePermission
from strawberry.types import Info
from Middleware.jwtmanager import JWTManager
from dotenv import find_dotenv, load_dotenv
import os


# Load dotenv
load_dotenv(find_dotenv(".env"))
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


class IsAuthenticated(BasePermission):
    message = "User is not Authenticated"

    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:

        # Get request,response object
        request = info.context["request"]
        res = info.context["response"]

        # Get redis object
        redis = info.context["redis_client"]
        acctoken = request.cookies.get("accessToken", None)
        refToken = request.cookies.get("refreshToken", None)

        if not acctoken or not refToken:
            return False

        else:
            # Check if acctoken valid
            isvalid = await JWTManager.verify_jwt_auth(acctoken)
            if isvalid[-1] == "Invalid Token":
                return False
            else:
                # Check if reftoken for this user exists in redis
                data = await JWTManager.get_token_data(acctoken)
                refToken_redis = await redis.get(data["userID"])

                # If no refToken_redis does not exists
                if not refToken_redis:
                    return False

                refToken_redis = json.loads(refToken_redis)

                # If refToken from redis and user do not match
                if refToken != refToken_redis["refToken"]:
                    return False

                # Check if refToken_user_valid and refToken_redis_valid
                refToken_user_valid = await JWTManager.verify_jwt_auth(refToken)
                if refToken_user_valid[-1] == "Invalid token":
                    return False

                refToken_redis_valid = await JWTManager.verify_jwt_auth(
                    refToken_redis["refToken"]
                )
                if refToken_redis_valid[-1] == "Invalid token":
                    return False

                if (
                    isvalid[-1] == "Token expired"
                    or refToken_redis_valid[-1] == "Token expired"
                ):
                    accToken = await JWTManager.generate_token({})
                    refToken = await JWTManager.generate_token(
                        {}, REFRESH_TOKEN_EXPIRE_MINUTES
                    )
                    res.set_cookie(
                        "accessToken", accToken, httponly=True, samesite="strict"
                    )
                    res.set_cookie(
                        "refreshToken", refToken, httponly=True, samesite="strict"
                    )
                    return True
        return True
