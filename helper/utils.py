from fastapi.encoders import jsonable_encoder
from email_validator import validate_email, EmailNotValidError

# Encode Inputs


def encode_input(data) -> dict:
    data = jsonable_encoder(data)
    tmp = {}
    for k, v in data.items():
        if v:
            tmp[k] = v
    return tmp


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
