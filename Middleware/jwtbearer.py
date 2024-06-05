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

        # Access headers authentication
        authentication = request.headers["authentication"]
        if authentication:
            token = authentication.split("Bearer ")[-1]
            isverified = await JWTManager.verify_jwt(token)
            if isverified:
                return True
            else:
                # refToken = request.cookies.get("refreshToken", None)
                data = await JWTManager.get_token_data(token)
                refToken = await redis.get(data["userID"])
                if not refToken:
                    return False
                else:
                    isRefTokenValid = await JWTManager.verify_jwt(refToken)
                    if not isRefTokenValid:
                        return False
                    else:
                        accToken = await JWTManager.generate_token({})
                        refToken = await JWTManager.generate_token(
                            {}, REFRESH_TOKEN_EXPIRE_MINUTES
                        )
                        res.headers["Authorization"] = accToken
                        res.set_cookie(
                            "refreshToken", refToken, httponly=True, samesite="strict"
                        )
                        return True

        return False
