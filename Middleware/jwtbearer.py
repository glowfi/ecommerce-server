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

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:

        # Get request,response object
        request = info.context["request"]
        res = info.context["response"]

        # Access headers authentication
        authentication = request.headers["authentication"]
        if authentication:
            token = authentication.split("Bearer ")[-1]
            isverified = JWTManager.verify_jwt(token)
            if isverified:
                return True
            else:
                refToken = request.cookies.get("refreshToken", None)
                if not refToken:
                    return False
                else:
                    isRefTokenValid = JWTManager.verify_jwt(refToken)
                    if not isRefTokenValid:
                        return False
                    else:
                        accToken = JWTManager.generate_token({})
                        refToken = JWTManager.generate_token(
                            {}, REFRESH_TOKEN_EXPIRE_MINUTES
                        )
                        res.headers["Authorization"] = accToken
                        res.set_cookie(
                            "refreshToken", refToken, httponly=True, samesite="strict"
                        )
                        return True

        return False
