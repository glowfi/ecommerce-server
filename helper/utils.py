from typing import DefaultDict
from fastapi.encoders import jsonable_encoder
from email_validator import validate_email, EmailNotValidError
from models.dbschema import Admin, Seller, User
import random
import string
from genderize import Genderize
from strawberry.permission import BasePermission
from strawberry.types import Info
import typing


# Encode Inputs


def encode_input(data) -> dict:
    data = jsonable_encoder(data)
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = encode_input(v)
        if v not in ("", None, {}, 0):
            new_data[k] = v
    return new_data


def generate_random_number(length):
    return int("".join([str(random.randint(0, 10)) for _ in range(length)]))


def generate_random_alphanumeric(length):
    lst = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
    return "".join(lst)


# Helper function checkUserExists


async def checkUserExists(email, userType):
    if userType == "admin":
        return await Admin.find({"email": email}).to_list()
    elif userType == "seller":
        return await Seller.find({"email": email}).to_list()
    elif userType == "user":
        return await User.find({"email": email}).to_list()


# Validate Email & Password


async def validate_mail(email) -> tuple[bool, str]:
    try:
        emailinfo = validate_email(email)
        return (True, str(emailinfo.normalized))

    except EmailNotValidError as e:
        return (False, str(e))


async def validate_password(password) -> tuple[bool, str]:
    if len(password) >= 8:
        return (True, "")
    else:
        return (False, "Password length must be greater than equal to 8")


async def validate_inputs(email, password) -> tuple[bool, str]:
    res_email, res_password = await validate_mail(email), await validate_password(
        password
    )
    if not res_email[0]:
        return res_email
    elif not res_password[0]:
        return res_password
    return (True, "")


def get_pics(name):
    pics_default = {
        "women": [
            "https://ui.shadcn.com/avatars/01.png",
            "https://ui.shadcn.com/avatars/03.png",
            "https://ui.shadcn.com/avatars/05.png",
        ],
        "men": [
            "https://ui.shadcn.com/avatars/02.png",
            "https://ui.shadcn.com/avatars/04.png",
        ],
    }

    gender = Genderize().get([name])[0]["gender"]
    if gender == "male":
        randIdx = random.randint(0, 1)
        return pics_default["men"][randIdx]
    else:
        randIdx = random.randint(0, 2)
        return pics_default["women"][randIdx]


class retval(BasePermission):
    message = "User is not Authenticated"

    async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return True
