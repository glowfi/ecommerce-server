from helper.password import verify_password
from models.dbschema import User
import strawberry
from Graphql.schema.auth import (
    InputGoogleLogin,
    InputLogin,
    Login,
    LoginResponse,
    LogoutResponse,
)
from Middleware.jwtmanager import JWTManager
from dotenv import find_dotenv, load_dotenv
import os

from helper.utils import checkUserExists, encode_input


# Load dotenv
load_dotenv(find_dotenv(".env"))
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


async def user_generate_token(checkUser, data, info):
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
    refToken = await JWTManager.generate_token(detail, REFRESH_TOKEN_EXPIRE_MINUTES)

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
    res.set_cookie("refreshToken", refToken, httponly=True, samesite="strict")

    print(checkUser[0].address)

    details = Login(
        **{
            **detail,
            "address": checkUser[0].address,
            "phone_number": checkUser[0].phone_number,
        }
    )

    return details


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
    async def login_google(
        self, data: InputGoogleLogin, info: strawberry.Info
    ) -> LoginResponse:

        # Check if user exists with google email
        user = await checkUserExists(data.email, data.userType)

        if user:
            print("User exits!")
            # generate token
            details = await user_generate_token(user, data, info)
            return LoginResponse(data=details, err=None)
        else:
            # if user do not exist then create user & generate_token
            encoded_data = encode_input(data.__dict__)
            address = {
                "street_address": "",
                "city": "",
                "state": "",
                "country": "",
                "countryCode": "",
                "zip_code": 0,
            }

            new_user = User(**encoded_data, address=address)
            user_ins = await new_user.insert()

            # generate token
            details = await user_generate_token([user_ins], data, info)
            return LoginResponse(data=details, err=None)

    @strawberry.mutation
    async def login(self, data: InputLogin, info: strawberry.Info) -> LoginResponse:
        if data.userType.lower() not in ["admin", "seller", "user"]:
            return LoginResponse(
                data=None, err="userType mut be admin or seller or user"
            )

        else:
            checkUser = await checkUserExists(data.email, data.userType)
            # print(data.password, checkUser[0].password)

            if not checkUser:
                return LoginResponse(
                    data=None,
                    err=f"No such user with email {data.email} exists as {data.userType}",
                )

            elif not checkUser[0].confirmed:
                return LoginResponse(
                    data=None, err=f"Verify your account before logging in!"
                )

            elif verify_password(data.password, checkUser[0].password) is False:
                return LoginResponse(data=None, err=f"Wrong Password entered!")

            else:
                details = await user_generate_token(checkUser, data, info)
                return LoginResponse(data=details, err=None)
