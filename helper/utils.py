from fastapi.encoders import jsonable_encoder


def encode_input(data) -> dict:
    data = jsonable_encoder(data)
    tmp = {}
    for k, v in data.items():
        if v:
            tmp[k] = v
    return tmp
