import strawberry
from models.dbschema import Admin, Seller, User
from Middleware.jwtmanager import JWTManager
from dotenv import find_dotenv, load_dotenv
import os


# Load dotenv
load_dotenv(find_dotenv(".env"))
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


@strawberry.input
class Data:
    email: str
    password: str
    userType: str


@strawberry.type
class Login:
    id: str
    accToken: str
    email: str
    userType: str


@strawberry.type
class LoginResponse:
    data: Login | None
    err: str | None


@strawberry.type
class RegisterResponse(LoginResponse):
    pass


async def checkUserExists(email, userType):
    if userType == "admin":
        return await Admin.find({"email": email}).to_list()
    elif userType == "seller":
        return await Seller.find({"email": email}).to_list()
    elif userType == "user":
        return await User.find({"email": email}).to_list()


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def login(self, data: Data, info: strawberry.Info) -> LoginResponse:
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

            else:
                # Generate Token
                detail = {
                    "id": str(res[0].id),
                    "email": data.email,
                    "userType": data.userType,
                }
                accToken = JWTManager.generate_token(detail)
                detail["accToken"] = accToken
                refToken = JWTManager.generate_token(
                    detail, REFRESH_TOKEN_EXPIRE_MINUTES
                )
                res = info.context["response"]
                res.headers["Authorization"] = accToken
                res.set_cookie(
                    "refreshToken", refToken, httponly=True, samesite="strict"
                )

                details = Login(**detail)
                return LoginResponse(data=details, err=None)
