import datetime
import random
from faker import Faker
import string
import json

fake = Faker()

pics = []
for i in range(1, 5):
    if i == 1 or i == 3 or i == 5:
        pics.append(f"https://ui.shadcn.com/avatars/0{i}.png")


class Seller:
    def __init__(self):
        self.email = f"{fake.first_name().lower()}.{fake.last_name().lower()}@{fake.domain_name()}"
        self.phonenumber = fake.phone_number()
        self.dob = (
            datetime.datetime.now()
            - datetime.timedelta(days=random.randint(365 * 20, 365 * 80))
        ).strftime("%Y-%m-%d")
        self.password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(12)
        )
        self.company_name = fake.company()
        self.company_address = {
            "street_address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "country": fake.country(),
            "countryCode": fake.country_code(),
            "zip_code": fake.zipcode(),
        }
        self.seller_name = f"{fake.first_name()} {fake.last_name()}"


with open("./dataset.json", "r") as fp:
    data = json.load(fp)

for prod in data:
    seller = Seller()
    prod["seller_info"] = {
        "email": seller.email,
        "phone_number": seller.phonenumber,
        "dob": seller.dob,
        "password": seller.password,
        "company_name": seller.company_name,
        "company_address": seller.company_address,
        "seller_name": seller.seller_name,
        "profile_pic": random.choice(pics),
    }


with open("dataset.json", "w") as fp:
    json.dump(data, fp)

# Generate user data
user_data = []
for i in range(10):
    tmp = {
        "email": fake.email(),
        "name": f"{fake.first_name()} {fake.last_name()}",
        "password": fake.password(length=12),
        "dob": str(fake.date_of_birth()),
        "phone_number": fake.phone_number(),
        "address": {
            "street_address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "country": fake.country(),
            "countryCode": fake.country_code(),
            "zip_code": fake.zipcode(),
        },
        "profile_pic": random.choice(pics),
    }

    user_data.append(tmp)

with open("user.json", "w") as fp:
    json.dump(user_data, fp)
