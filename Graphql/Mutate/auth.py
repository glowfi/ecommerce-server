import strawberry
from models.dbschema import Admin, Seller, User


@strawberry.input
class Data:
    email: str
    password: str
    userType: str


@strawberry.type
class Login:
    id: str
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
    async def login(self, data: Data) -> LoginResponse:
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
                details = Login(
                    id=res[0].id,
                    email=data.email,
                    userType=data.userType,
                )
                return LoginResponse(data=details, err=None)
